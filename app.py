import os
import subprocess
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# 1. Secure Database Connection
MONGO_URI = "mongodb+srv://dbUser:ZI2OhyUIFgxAY6CR@cluster0.e96ydoo.mongodb.net/?appName=Cluster0"
try:
    client = MongoClient(MONGO_URI)
    db = client['quant_database']
    logs_collection = db['calculation_logs']
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"MongoDB Connection Warning: {e}")

@app.route('/analyze', methods=['POST'])
def analyze():
    req_data = request.get_json()
    if not req_data or 'operation' not in req_data or 'data' not in req_data:
        return jsonify({"error": "Invalid input layout. Provide 'operation' and 'data'."}), 400

    operation = req_data['operation']
    input_data = req_data['data']

    # Convert numeric list to space-separated string for C++ process
    data_str = " ".join(map(str, input_data))
    input_to_cpp = f"{operation} {len(input_data)} {data_str}\n"

    try:
        # 2. Run the compiled C++ Binary Engine
        process = subprocess.Popen(
            ['./quant_engine'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=input_to_cpp, timeout=5)

        if process.returncode != 0:
         return jsonify({
             "error": "C++ Engine Execution Failure",
             "stderr_log": stderr,
             "stdout_log": stdout,
             "data_sent_to_cpp": input_to_cpp
         }), 500

        # Parse output from C++ engine
        result = json.loads(stdout.strip())

        # 3. Log results to MongoDB Atlas Database
        log_document = {
            "operation": operation,
            "input_data": input_data,
            "output_result": result,
            "timestamp": os.getloadavg() # simple metric or omitted for speed
        }
        try:
            logs_collection.insert_one(log_document)
        except Exception as db_err:
            print(f"Database logging failed: {db_err}")

        return jsonify(result)

    except subprocess.TimeoutExpired:
        process.kill()
        return jsonify({"error": "C++ processing operation timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
