def convert_t2c(file=None):
    if file is None:
        print("ERROR: Txt content is blank, cannot process")
        return None

    import pandas as pd
    import io
    import re

    # Read the file content as text
    content = file.read().decode('utf-8')
    lines = content.split('\n')
    
    # Skip the first 9 rows (headers, error messages, report metadata)
    data_lines = lines[9:]
    
    # Filter out empty lines
    data_lines = [line.strip() for line in data_lines if line.strip()]
    
    # Parse each line into columns
    parsed_data = []
    for line in data_lines:
        # Skip total rows
        if 'TOTAL' in line.upper():
            continue
            
        # Split by whitespace and handle the complex structure
        parts = line.split()
        if len(parts) >= 8:
            # Field 1: G/L Acct # (format X.XXX)
            acct_num = parts[0]
            
            # Field 2: Type (format XX)
            acct_type = parts[1]
            
            # Field 3: Description (string format)
            # Find where the description ends by looking for the Starting Balance pattern
            desc_parts = []
            i = 2
            
            # Look ahead to see if we have enough parts for a complete row
            # We need at least 8 total parts: acct_num, type, description, starting_bal, debit, credit, net, ending
            if len(parts) >= 8:
                # Look for the pattern: after description, we should have 5 consecutive financial values
                # starting_bal, debit, credit, net, ending
                for j in range(2, len(parts) - 4):
                    # Check if from position j onwards we have 5 consecutive financial values
                    financial_count = 0
                    for k in range(j, min(j + 5, len(parts))):
                        part = parts[k]
                        # Check if this looks like a financial value
                        if (part == '0.00' or 
                            re.match(r'^\d{1,3}(,\d{3})*\.\d{2}[DR]{2}', part) or
                            re.match(r'^\d{1,3}(,\d{3})*\.\d{2}[CR]{2}', part) or
                            re.match(r'^\d{1,3}(,\d{3})*\.\d{2}', part) or 
                            re.match(r'^(\d{1,3})*\.\d{2}', part)):
                            financial_count += 1
                        else:
                            break
                    
                    # If we found 5 consecutive financial values starting at position j, 
                    # then the description ends at position j-1
                    if financial_count == 5:
                        i = j
                        break
            
            # Build description from parts 2 to i-1
            description = ' '.join(parts[2:i])
            
            # Extract the numerical values starting from position i
            numerical_values = parts[i:]
            
            if len(numerical_values) >= 5:
                # Extract ending balance and DR/CR
                ending_balance_str = numerical_values[4]
                
                # Parse ending balance
                if ending_balance_str == '0.00':
                    ending_balance_num = 0.0
                    dr_cr = ''
                else:
                    # Extract the number and DR/CR suffix
                    match = re.match(r'^(\d{1,3}(,\d{3})*\.\d{2})([DR]{2}|[CR]{2})$', ending_balance_str)
                    if match:
                        number_str = match.group(1).replace(',', '')
                        dr_cr = match.group(3)
                        ending_balance_num = float(number_str)
                        if dr_cr == 'CR':
                            ending_balance_num = -ending_balance_num
                    else:
                        # Fallback: try to extract just the number
                        number_str = ending_balance_str.replace(',', '')
                        if re.match(r'^\d+\.\d{2}$', number_str):
                            ending_balance_num = float(number_str)
                            dr_cr = ''
                        else:
                            ending_balance_num = 0.0
                            dr_cr = ''
                
                row_data = [
                    acct_num,                     # Field 1: X.XXX
                    acct_type,                    # Field 2: XX
                    description,                  # Field 3: string
                    ending_balance_num,           # Field 4: Ending Balance (number)
                    dr_cr                         # Field 5: DR/CR
                    ]
                parsed_data.append(row_data)
    
    # Create DataFrame with proper column headers
    df = pd.DataFrame(parsed_data, columns=[
        "G/L Acct #",
        "Type", 
        "Description", 
        "Ending Balance", 
        "DR/CR"
    ])
    
    # Convert all columns to strings except Ending Balance
    for col in df.columns:
        if col != "Ending Balance":
            df[col] = df[col].astype(str)
    
    # Create a new file-like object for the CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    print(f"Successfully converted {len(df)} rows to CSV")
    print(f"Here is the first three rows converted:")
    print("Headers:", list(df.columns))
    print("First row:", df.iloc[0].tolist() if len(df) > 0 else "No data")
    print("Second row:", df.iloc[1].tolist() if len(df) > 1 else "No second row")
    return csv_buffer
