from flask import Flask, jsonify, render_template
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

if __name__ == '__main__':
  app.run(port=8000)