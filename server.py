from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/submit', methods=['POST'])
def submit_data():
  data = request.get_json()

  print(data)

  return jsonify(data)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000)