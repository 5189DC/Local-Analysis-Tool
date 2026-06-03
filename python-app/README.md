# Local Analysis Tool Python App

This is the larger-file version of Local Analysis Tool.

It still opens in your browser, but Python does the CSV work locally on your computer. Your CSV is not uploaded to the internet.

## Which App Should I Use?

Use `Local Analysis Tool.html` for normal CSV files because it is easiest.

Use this Python app when the CSV is very large or the HTML version feels slow.

## macOS: First Time Setup

You only need to do this once.

1. Open the `python-app` folder in Finder.
2. Right-click the folder and choose `New Terminal at Folder`.
3. Paste this into Terminal and press `Return`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If `New Terminal at Folder` is not available:

1. Open Terminal.
2. Type `cd ` with a space after it.
3. Drag the `python-app` folder into Terminal.
4. Press `Return`.
5. Then run the setup commands above.

## macOS: Open the App After Setup

Every time you want to use the Python app:

1. Open the `python-app` folder in Finder.
2. Right-click the folder and choose `New Terminal at Folder`.
3. Paste this into Terminal and press `Return`:

```bash
source .venv/bin/activate
streamlit run app.py
```

A browser page should open automatically. If it does not, copy the local address shown in Terminal, usually:

```text
http://localhost:8501
```

## macOS: Put a CSV Path Into the App

The easiest way is to use the upload button in the app.

If you want to use the local CSV path box instead:

1. Find the CSV file in Finder.
2. Right-click the CSV file.
3. Hold the `Option` key.
4. Click `Copy "filename.csv" as Pathname`.
5. Paste it into the local CSV path box.

The path must be the CSV file itself, not just the folder.

Example:

```text
/Users/denver/Documents/Code/Local Analysis Tool/Fuel-Table.csv
```

## Windows: First Time Setup

You only need to do this once.

1. Open the `python-app` folder in File Explorer.
2. Click the address bar.
3. Type `powershell` and press `Enter`.
4. Paste this into PowerShell and press `Enter`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If Windows blocks the activation command, run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then try this again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Windows: Open the App After Setup

1. Open the `python-app` folder in File Explorer.
2. Click the address bar.
3. Type `powershell` and press `Enter`.
4. Paste this into PowerShell and press `Enter`:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

## Using the App

1. Upload a CSV, or paste the full path to a CSV file.
2. If row 2 contains units, leave `Detect row 2 as units` turned on.
3. Choose the `X axis`.
4. Choose one or more numeric `Y columns`.
5. Use `Graph drag action` to choose whether dragging zooms or pans.
6. Use the mouse wheel or touchpad over the chart to zoom.
7. Use `Plot row limit` and `Plot every Nth row` for very large CSV files.

When multiple Y columns are selected, each series gets its own colored Y axis and title.
