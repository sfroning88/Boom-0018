import os, sys
from flask import Flask, render_template, request, jsonify
from ngrok import connect

# create a Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# get the Ngrok token
ngrok_token = os.environ.get('NGROK_API_TOKEN')

@app.route('/')
def home():
    # render base home template
    return render_template('chat.html')

# upload the txt file
@app.route('/UPLOAD_TXT_FILE', methods=['POST'])
def UPLOAD_TXT_FILE():
    file = request.files.get('file')
    if not file:
            return jsonify({'success': False, 'message': 'No file detected.'}), 400

    from support.extension import ALLOWED_EXTENSIONS, retrieve_extension
    if retrieve_extension(file.filename) not in ALLOWED_EXTENSIONS:
        return jsonify({'success': False, 'message': 'Incorrect filetype uploaded.'}), 400

    from functions.t2c import convert_t2c
    converted_file = convert_t2c(file=file)

    if converted_file is None:
        print(f"ERROR: File was not converted into csv successfully")
        return jsonify({'success': False, 'message': 'Could not convert to csv.'}), 400

    from functions.c2x import convert_c2x
    converted_file = convert_c2x(converted_file=converted_file)

    if converted_file is None:
        print(f"ERROR: File was not converted into xlsx successfully")
        return jsonify({'success': False, 'message': 'Could not convert to xlsx.'}), 400

    from support.generate import generate_code
    code = generate_code(file.filename)

    import support.config
    support.config.files[code] = {'filename': file.filename, 'content': converted_file}

    return jsonify({'success': True, 'message': 'Uploading txt file success.'}), 200

# download the xlsx file
@app.route('/DOWNLOAD_XLSX_FILE', methods=['POST'])
def DOWNLOAD_XLSX_FILE():
    import support.config
    from tqdm import tqdm
    import os
    
    if not support.config.files:
        return jsonify({'success': False, 'message': 'No files available for download.'}), 400
    
    # Create downloads directory if it doesn't exist
    downloads_dir = os.path.expanduser("~/Downloads")
    if not os.path.exists(downloads_dir):
        downloads_dir = os.getcwd()  # Fallback to current directory
    
    print(f"Starting download of {len(support.config.files)} files...")
    
    # Download each file with progress bar
    for code, file_info in tqdm(support.config.files.items(), desc="Downloading files"):
        filename = file_info['filename']
        content = file_info['content']
        
        # Generate Excel filename
        excel_filename = os.path.splitext(filename)[0] + '.xlsx'
        file_path = os.path.join(downloads_dir, excel_filename)
        
        try:
            # Reset buffer position and write to file
            content.seek(0)
            with open(file_path, 'wb') as f:
                f.write(content.read())
            print(f"Downloaded: {excel_filename}")
        except Exception as e:
            print(f"ERROR: Could not download {excel_filename}: {e}")
    
    print("Download complete!")
    return jsonify({'success': True, 'message': f'Downloaded {len(support.config.files)} files to {downloads_dir}'}), 200
    
if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage: python3 app.py")
        sys.exit(1)

    # ngrok tunnel URL (will be set when tunnel is created)
    ngrok_url = None

    # Check if ngrok is available and create tunnel
    import importlib.util
    ngrok_spec = importlib.util.find_spec("ngrok")
    
    if ngrok_spec is None:
        print("ERROR: ngrok package not available")
        sys.exit(1)

    # Authenticate with ngrok using environment token
    if ngrok_token is None:
        print("ERROR: Please set your ngrok token")
        sys.exit(1)
    
    from ngrok import set_auth_token
    set_auth_token(ngrok_token)

    from ngrok import connect
    tunnel = connect(5000, domain="guiding-needlessly-mallard.ngrok-free.app")

    if tunnel is None:
        print("ERROR: Failed to connect to ngrok tunnel, check active instances")
        sys.exit(1)

    print("##############################_APP_BEGIN_##############################")

    # dictionary for uploaded files
    import support.config
    support.config.files = {}
    print(f"CHECKPOINT: Files dictionary initialized: {'Yes' if support.config.files is not None else 'No'}")

    print(f"CHECKPOINT: Using static domain: https://guiding-needlessly-mallard.ngrok-free.app/oauth/callback")
    
    print("##############################_APP_END_##############################")

    # run the app
    app.run(port=5000)
