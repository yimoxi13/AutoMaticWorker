from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# 允许跨域请求, vue默认端口为5173而flask默认为5000
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Hello from Flask backend!"
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)