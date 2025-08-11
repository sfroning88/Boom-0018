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
    import support.config
    from support.extension import ALLOWED_EXTENSIONS, retrieve_extension
    from support.generate import generate_code
    
    file = request.files.get('file')
    if not file:
            return jsonify({'success': False, 'message': 'No file detected.'}), 400

    code = generate_code(file.filename)

    exte = retrieve_extension(file.filename)
    if exte not in ALLOWED_EXTENSIONS:
        return jsonify({'success': False, 'message': 'Incorrect filetype uplaoded.'}), 400

    return jsonify({'success': True, 'message': 'Uplaoding txt file success.'}), 200

# download the xlsx file
@app.route('/DOWNLOAD_XLSX_FILE', methods=['POST'])
def DOWNLOAD_XLSX_FILE():
    try:
        return jsonify({'success': True, 'message': 'Downloading xlsx file success.'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    
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
