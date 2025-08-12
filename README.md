# Boom-0018
A simple tool that converts legacy accounting system text files into clean Excel spreadsheets. This tool automatically processes multiple text files and extracts key financial data into organized columns.

## What This Tool Does

This tool takes text files from legacy accounting systems and converts them through a two-step process:
1. **Text → CSV**: Extracts specific data columns from the text files
2. **CSV → Excel**: Converts the CSV data into Excel (.xlsx) format

## How It Works

### Step 1: Upload Text Files
- Click the **"Upload Folder"** button (orange button)
- Select a folder containing your text (.txt) files
- The tool will process all text files in the folder
- It automatically skips the first 9 rows (headers and metadata)
- Extracts these 5 key columns:
  - **G/L Acct #** (Account number in X.XXX format)
  - **Type** (Account type in XX format)
  - **Description** (Account description)
  - **Ending Balance** (Numerical balance amount)
  - **DR/CR** (Debit/Credit indicator)

### Step 2: Download Excel Files
- Click the **"Download Xlsx File"** button (green button)
- Enter the folder path where you want your Excel files saved
- The tool will download all converted Excel files to your specified location
- Files maintain their original names but with .xlsx extension
- Subfolder structure is preserved if your original folder had subfolders

## File Processing Details

### Text File Requirements
- Files must be .txt format
- Should contain accounting data with consistent formatting
- First 9 rows are automatically skipped (headers/metadata)
- Data should have at least 8 columns of information

### Data Extraction Rules
- **Account Numbers**: Extracted in X.XXX format
- **Account Types**: Extracted as XX format codes
- **Descriptions**: All text between account type and financial values
- **Financial Values**: Automatically detects and parses ending balances
- **DR/CR Indicators**: Extracted from the ending balance field

### Output Format
- Clean Excel files with 5 organized columns
- All data properly formatted and aligned
- Ready for analysis in Excel or other spreadsheet applications

## Usage Instructions

1. **Start the Tool**: Run `python3 app.py` in your terminal
2. **Open Your Browser**: Navigate to the provided URL
3. **Upload Files**: Click "Upload Folder" and select your text file folder
4. **Wait for Processing**: The tool will show progress as it converts files
5. **Download Results**: Click "Download Xlsx File" and specify your download location
6. **Access Your Files**: Find your converted Excel files in the specified folder

## Technical Notes for Support

- **Supported Formats**: .txt input → .csv intermediate → .xlsx output
- **Data Processing**: Skips metadata rows, filters totals, parses financial values
- **File Handling**: Processes entire folders, maintains subfolder structure
- **Error Handling**: Continues processing if individual files fail
- **Memory Management**: Uses buffers for efficient file processing

## Troubleshooting

- **No Files Processed**: Ensure your text files have the expected format
- **Download Errors**: Check that the download path exists and is writable
- **Processing Failures**: Verify text files contain valid accounting data
- **Browser Issues**: Try refreshing the page if buttons become unresponsive

## For Cursor AI Assistant

When helping users with this tool, understand that:
- The workflow is: Upload Folder → Process Text Files → Convert to CSV → Convert to Excel → Download
- Files are stored in a global dictionary (`support.config.files`) after processing
- The download function processes all files in this global dictionary
- Text files are parsed using specific rules for accounting data extraction
- The tool automatically handles file format validation and error recovery
