from flask import Flask, request, jsonify
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    content = request.json
    operation = content.get('operation')
    data = content.get('data')

    if not operation or not data:
        return jsonify({"error": "Missing parameters"}), 400

    # Get absolute path to the .exe file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(base_dir, 'quant_engine.exe')

    # Double check if the file actually exists in this folder
    if not os.path.exists(exe_path):
        return jsonify({
            "error": f"quant_engine.exe not found in {base_dir}. Current files: {os.listdir(base_dir)}"
        }), 404

    # Fix for OneDrive: Build the command as a single string and wrap paths in quotes
    data_str = " ".join(map(str, data))
    cmd = f'"{exe_path}" {operation} {data_str}'
    
    try:
        # shell=True forces Windows to resolve OneDrive virtual paths correctly
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        
        # If C++ executed but returned an empty string or error
        if not result.stdout.strip():
            return jsonify({"error": "C++ engine returned no output", "stderr": result.stderr}), 500
            
        return jsonify(json.loads(result.stdout))
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)