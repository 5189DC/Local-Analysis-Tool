# Local Analysis Tool

Current version: `v1.0`

A local CSV plotting tool for quick data inspection. It runs in your browser from a single HTML file and does not need an internet connection, server, or install.

## v1.0

This release includes:

- CSV import from file picker or drag and drop.
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

## Open the App

Double-click `Open Local Analysis Tool.command`, or double-click `Local Analysis Tool.html`.

If macOS asks for permission to run the `.command` file, you can open the HTML file directly instead.

## Use It

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

## Notes

The data preview shows all loaded rows and all columns. Very large CSV files may take a moment to render in the preview table.
