# Local Analysis Tool

Current version: `v0.0`

A local CSV plotting tool for quick data inspection. It runs in your browser from a single HTML file and does not need an internet connection, server, or install.

## v0.0

This first version includes:

- CSV import from file picker or drag and drop.
- Automatic X-axis detection for date/time columns.
- Manual column selection, with no series selected by default.
- Smarter X-axis labels that update when the chart is zoomed.
- More Y-axis tick labels when multiple columns are selected.
- Chart zoom by left-click drag, with `Reset`, `Fit X`, and `Fit Y` controls.
- Optional X-axis sorting and gap connection.
- Full data preview table with scrollable rows and columns.
- PNG export for the current chart.

## Open the App

Double-click `Open Local Analysis Tool.command`, or double-click `Local Analysis Tool.html`.

If macOS asks for permission to run the `.command` file, you can open the HTML file directly instead.

## Use It

1. Click `+ CSV` or drop a CSV file onto the app.
2. Choose any column for the `X axis`. This can be a date, number, or text column.
3. Choose any number of numeric columns to plot.
4. Use `Sort X axis` when the X axis is a date or number.
5. Left-click and drag across the chart to zoom into an area.
6. Right-click the chart to zoom back out one step.
7. Use `Fit X` to restore the full X axis while keeping the current Y view.
8. Use `Connect gaps` if the data has blanks and you want lines to continue across missing values.
9. Click `PNG` to save the current chart image.

## Apple Numbers Files

The app reads CSV files. For a `.numbers` file, open it in Apple Numbers first, then use `File > Export To > CSV`, and import the exported CSV into this app.

## Notes

The data preview shows all loaded rows and all columns. Very large CSV files may take a moment to render in the preview table.
