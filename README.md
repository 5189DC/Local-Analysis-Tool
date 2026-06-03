# Local Analysis Tool

Current version: `v1.1`

A local CSV plotting tool for quick data inspection. The project now has two local versions:

- `Local Analysis Tool.html` for simple sharing and normal CSV files.
- `python-app/` for heavier CSV files that need a local Python helper.

Both versions run locally on your computer. Your CSV data is not uploaded to the internet.

## Which Version Should I Use?

Use the HTML app when you want the easiest option:

- Open `Local Analysis Tool.html` directly.
- No install.
- Good for normal CSV files.
- Best for sharing with people who do not want to use Terminal.

Use the Python app when the CSV is large or the HTML version feels slow:

- Open the app through Terminal.
- Uses Streamlit and DuckDB locally.
- Better for larger CSV previewing, row limits, sampling, and plotting.
- Setup instructions are in `python-app/README.md`.

## v1.1

This release adds the separate Python app for heavier CSV files while keeping the original HTML app.

The HTML app includes:

- CSV import from file picker or drag and drop.
- Automatic row 2 unit detection for CSVs that put units below the header row.
- Automatic X-axis detection for date/time columns.
- Manual column selection, with no series selected by default.
- Separate resizable graph window, with a `Graph` button to reopen it.
- Separate Y axes for multiple selected columns, with axis titles above each axis.
- Smarter X-axis labels that update when the chart is zoomed or resized.
- Chart zoom by left-click drag and trackpad pinch.
- Chart panning by normal scrolling or right-click drag.
- Chart controls for `Reset`, label size, `Fit X`, `Fit Y`, `PNG`, and `Close`.
- Light and night mode toggle, remembered between sessions.
- Optional X-axis sorting and gap connection.
- Full data preview table with scrollable rows and columns.
- PNG export for the current chart, always on a white background.

The Python app includes:

- CSV upload or local CSV path input.
- DuckDB-backed previewing for larger CSV files.
- Row 2 unit detection.
- Preview row limits and plot row limits.
- Plot every Nth row sampling for large charts.
- Zoom/pan chart interactions.
- Separate colored Y axes for multiple selected columns.

## Open the HTML App

Double-click `Local Analysis Tool.html`.

## Open the Python App

Use this for heavier CSV files.

Read `python-app/README.md` for beginner-friendly macOS and Windows setup steps.

## Use the HTML App

1. Click `+ CSV` or drop a CSV file onto the app.
2. Choose any column for the `X axis`. This can be a date, number, or text column.
3. Choose any number of numeric columns to plot.
4. Use `Sort X axis` when the X axis is a date or number.
5. Click `Graph` to open the chart in a separate resizable window.
6. Left-click and drag across the chart to zoom into an area.
7. Use trackpad pinch to zoom in or out around the pointer.
8. Scroll normally or right-click drag to pan around a zoomed chart.
9. Right-click without dragging to step back through zoom history.
10. Use `Fit X` to restore the full X axis while keeping the current Y view.
11. Use `Connect gaps` if the data has blanks and you want lines to continue across missing values.
12. Click `PNG` in the graph window to save the current chart image.

## Apple Numbers Files

The app reads CSV files. For a `.numbers` file, open it in Apple Numbers first, then use `File > Export To > CSV`, and import the exported CSV into this app.

## CSV Unit Rows

If row 2 looks like a units row, the app treats it as metadata instead of data. For example, headers in row 1 and units like `mile`, `GBP`, or `%` in row 2 will make the preview and chart start from row 3, while labels show units such as `Odometer (mile)`.

## Notes

The data preview shows all loaded rows and all columns. Very large CSV files may take a moment to render in the preview table.
