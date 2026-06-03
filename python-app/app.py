from __future__ import annotations

import csv
import re
import shlex
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

import duckdb
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


APP_TITLE = "Local Analysis Tool"
APP_VERSION = "v1.1 Python"
DEFAULT_PREVIEW_ROWS = 500
DEFAULT_PLOT_ROWS = 10000
CHART_COLORS = [
    "#176b87", "#c75146", "#2f7d55", "#8357a8", "#d08b21",
    "#2267b1", "#b33f83", "#60712f", "#6c5b4c", "#18827d",
]


def clean_header(value: Any, index: int) -> str:
    text = str(value or "").strip()
    return text or f"Column {index + 1}"


def quote_ident(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def parse_number(value: Any) -> float | None:
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    normalized = re.sub(r"[£$€¥,\s]", "", raw)
    normalized = re.sub(r"%$", "", normalized)
    normalized = re.sub(r"[^\d.+\-eE]", "", normalized)
    if normalized in {"", "-", "."}:
        return None
    try:
        return float(normalized)
    except ValueError:
        return None


def is_likely_unit_cell(value: Any) -> bool:
    raw = str(value or "").strip()
    if not raw:
        return False
    if parse_number(raw) is not None:
        return False
    if len(raw) > 24:
        return False
    if re.search(r"[,;:]", raw):
        return False
    if re.search(r"\s", raw) and not re.fullmatch(r"(?i)(per|each|total|average|avg)", raw):
        return False
    return bool(re.search(r"[A-Za-z%°£$€¥/²³µμ-]", raw))


def inspect_csv(path: Path) -> tuple[list[str], dict[str, str], bool, int]:
    with path.open("r", newline="", encoding="utf-8-sig", errors="replace") as handle:
        reader = csv.reader(handle)
        first_rows = []
        for row in reader:
            if any(cell.strip() for cell in row):
                first_rows.append(row)
            if len(first_rows) >= 3:
                break

    if len(first_rows) < 2:
        raise ValueError("CSV needs a header row and at least one data row.")

    headers = [clean_header(value, index) for index, value in enumerate(first_rows[0])]
    if len(first_rows) < 3:
        return headers, {}, False, 0

    candidate = first_rows[1]
    first_data = first_rows[2]
    populated = 0
    unit_like = 0
    first_data_values = 0

    for index, _header in enumerate(headers):
        unit = str(candidate[index] if index < len(candidate) else "").strip()
        if unit:
            populated += 1
        if is_likely_unit_cell(unit):
            unit_like += 1
        data_value = first_data[index] if index < len(first_data) else ""
        if parse_number(data_value) is not None or pd.notna(pd.to_datetime(data_value, errors="coerce")):
            first_data_values += 1

    populated_ratio = populated / max(1, len(headers))
    unit_ratio = unit_like / max(1, populated)
    data_ratio = first_data_values / max(1, len(headers))
    has_unit_row = populated >= 1 and populated_ratio >= 0.3 and unit_ratio >= 0.7 and data_ratio >= 0.3
    if not has_unit_row:
        return headers, {}, False, 0

    units = {}
    for index, header in enumerate(headers):
        unit = str(candidate[index] if index < len(candidate) else "").strip()
        if is_likely_unit_cell(unit):
            units[header] = unit
    return headers, units, True, 1


def display_header(header: str, units: dict[str, str]) -> str:
    unit = units.get(header)
    return f"{header} ({unit})" if unit else header


def save_upload(uploaded_file: Any) -> Path:
    suffix = Path(uploaded_file.name).suffix or ".csv"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as handle:
        handle.write(uploaded_file.getbuffer())
        return Path(handle.name)


def normalize_local_path(raw_path: str) -> Path:
    text = raw_path.strip()
    if not text:
        return Path()

    if text.startswith("file://"):
        parsed = urlparse(text)
        text = unquote(parsed.path)
    else:
        try:
            parts = shlex.split(text)
            if len(parts) == 1:
                text = parts[0]
        except ValueError:
            text = text.strip("'\"")

    return Path(text).expanduser()


def read_preview(con: duckdb.DuckDBPyConnection, path: Path, data_offset: int, limit: int) -> pd.DataFrame:
    return con.execute(
        "select * from read_csv_auto(?, header=true, all_varchar=true, ignore_errors=true) limit ? offset ?",
        [str(path), limit, data_offset],
    ).df()


def get_count(con: duckdb.DuckDBPyConnection, path: Path, data_offset: int) -> int:
    return con.execute(
        "select count(*) from (select * from read_csv_auto(?, header=true, all_varchar=true, ignore_errors=true) offset ?)",
        [str(path), data_offset],
    ).fetchone()[0]


def get_plot_data(
    con: duckdb.DuckDBPyConnection,
    path: Path,
    data_offset: int,
    x_column: str,
    y_columns: list[str],
    row_limit: int,
    sample_every: int,
) -> pd.DataFrame:
    columns = [x_column, *y_columns]
    selected = ", ".join(quote_ident(column) for column in columns)
    query = f"""
        select {selected}
        from read_csv_auto(?, header=true, all_varchar=true, ignore_errors=true)
        where {quote_ident(x_column)} is not null
        limit ? offset ?
    """
    frame = con.execute(query, [str(path), row_limit * sample_every, data_offset]).df()
    if sample_every > 1:
        frame = frame.iloc[::sample_every].copy()
    for column in y_columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame.dropna(subset=y_columns, how="all")


def make_chart(
    plot_frame: pd.DataFrame,
    x_column: str,
    y_columns: list[str],
    units: dict[str, str],
    drag_mode_label: str,
) -> go.Figure:
    fig = go.Figure()
    axis_count = max(1, len(y_columns))
    axis_spacing = 0.055
    inner_axis_position = 0.12
    left_domain = min(inner_axis_position + axis_spacing * max(0, axis_count - 1), 0.42)

    for index, column in enumerate(y_columns):
        color = CHART_COLORS[index % len(CHART_COLORS)]
        axis_id = "y" if index == 0 else f"y{index + 1}"
        axis_key = "yaxis" if index == 0 else f"yaxis{index + 1}"
        position = left_domain - axis_spacing * index

        fig.add_trace(
            go.Scatter(
                x=plot_frame[x_column],
                y=plot_frame[column],
                mode="lines+markers",
                name=display_header(column, units),
                yaxis=axis_id,
                line={"color": color, "width": 2.4},
                marker={"color": color, "size": 5},
                hovertemplate=(
                    f"{display_header(x_column, units)}=%{{x}}<br>"
                    f"{display_header(column, units)}=%{{y}}<extra></extra>"
                ),
            )
        )

        axis_config = {
            "title": {
                "text": display_header(column, units),
                "font": {"color": color, "size": 12},
                "standoff": 8,
            },
            "tickfont": {"color": color, "size": 11},
            "linecolor": color,
            "linewidth": 2,
            "showline": True,
            "zeroline": False,
            "fixedrange": False,
            "automargin": True,
            "anchor": "free",
            "side": "left",
            "position": max(0, min(left_domain, position)),
        }
        if index > 0:
            axis_config["overlaying"] = "y"
            axis_config["showgrid"] = False
        fig.update_layout(**{axis_key: axis_config})

    fig.update_layout(
        height=620,
        dragmode="pan" if drag_mode_label == "Pan" else "zoom",
        xaxis={
            "title": display_header(x_column, units),
            "domain": [left_domain, 1],
            "fixedrange": False,
            "automargin": True,
        },
        legend={"orientation": "h", "y": -0.18},
        margin={"l": 24, "r": 24, "t": 24, "b": 96},
        hovermode="x unified",
    )
    return fig


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(f"{APP_TITLE} {APP_VERSION}")
    st.caption("Large CSV version. Runs locally with Streamlit and DuckDB.")

    with st.sidebar:
        st.header("CSV")
        uploaded = st.file_uploader("Upload CSV", type=["csv"])
        local_path = st.text_input("Or local CSV path")
        detect_units = st.checkbox("Detect row 2 as units", value=True)
        preview_rows = st.number_input("Preview rows", min_value=50, max_value=10000, value=DEFAULT_PREVIEW_ROWS, step=50)
        plot_rows = st.number_input("Plot row limit", min_value=100, max_value=1_000_000, value=DEFAULT_PLOT_ROWS, step=1000)
        sample_every = st.number_input("Plot every Nth row", min_value=1, max_value=10000, value=1, step=1)

    csv_path: Path | None = None
    if uploaded is not None:
        csv_path = save_upload(uploaded)
    elif local_path.strip():
        csv_path = normalize_local_path(local_path)

    if csv_path is None:
        st.info("Upload a CSV or enter a local CSV path.")
        return
    if not csv_path.exists():
        st.error(f"File not found: {csv_path}")
        st.caption("Tip: use the full file path, not just the folder path. On macOS Finder, right-click the CSV, hold Option, then choose Copy as Pathname.")
        return
    if csv_path.is_dir():
        st.error(f"This is a folder, not a CSV file: {csv_path}")
        st.caption("Choose the CSV file inside the folder, for example `/Users/name/Documents/data.csv`.")
        return

    try:
        headers, units, has_unit_row, data_offset = inspect_csv(csv_path)
    except Exception as error:
        st.error(str(error))
        return

    if not detect_units:
        units = {}
        has_unit_row = False
        data_offset = 0

    con = duckdb.connect()
    total_rows = get_count(con, csv_path, data_offset)
    if has_unit_row:
        st.success(f"Detected row 2 as units. Using {total_rows:,} data rows from row 3 onward.")
    else:
        st.success(f"Loaded {total_rows:,} data rows.")

    preview = read_preview(con, csv_path, data_offset, int(preview_rows))
    if preview.empty:
        st.warning("No rows to preview.")
        return

    columns = list(preview.columns)
    labeled_columns = {display_header(column, units): column for column in columns}
    reverse_labels = {column: display_header(column, units) for column in columns}

    st.subheader("Data Preview")
    st.dataframe(preview.rename(columns=reverse_labels), use_container_width=True, height=320)

    numeric_columns = [
        column for column in columns
        if pd.to_numeric(preview[column], errors="coerce").notna().sum() > 0
    ]
    if not numeric_columns:
        st.warning("No numeric columns found in the preview.")
        return

    st.subheader("Chart")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        x_label = st.selectbox("X axis", list(labeled_columns.keys()))
        y_labels = st.multiselect(
            "Y columns",
            [reverse_labels[column] for column in numeric_columns if column != labeled_columns[x_label]],
        )
        drag_mode_label = st.radio(
            "Graph drag action",
            ["Zoom box", "Pan"],
            horizontal=True,
            help="Touchpad or mouse-wheel zoom is enabled for both modes.",
        )

    if not y_labels:
        st.info("Choose at least one Y column.")
        return

    x_column = labeled_columns[x_label]
    y_columns = [labeled_columns[label] for label in y_labels]
    plot_frame = get_plot_data(con, csv_path, data_offset, x_column, y_columns, int(plot_rows), int(sample_every))
    if plot_frame.empty:
        st.warning("No plottable rows found for the selected columns.")
        return

    fig = make_chart(plot_frame, x_column, y_columns, units, drag_mode_label)
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "scrollZoom": True,
            "displaylogo": False,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "local-analysis-chart",
                "height": 900,
                "width": 1400,
                "scale": 1,
            },
        },
    )

    csv_download = plot_frame.rename(columns=reverse_labels).to_csv(index=False).encode("utf-8")
    st.download_button("Download plotted data", csv_download, "plotted-data.csv", "text/csv")


if __name__ == "__main__":
    main()
