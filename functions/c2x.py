def convert_c2x(converted_file=None):
    if converted_file is None:
        print("ERROR: Csv content is blank, cannot process")
        return None

    import pandas as pd
    import io

    # Read the CSV content from the StringIO buffer
    converted_file.seek(0)  # Reset buffer position
    df = pd.read_csv(converted_file)
        
    # Create a new Excel file buffer
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
        
    print(f"Successfully converted CSV to Excel with {len(df)} rows")
    return excel_buffer
