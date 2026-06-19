from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def handle_voice():
    print("קיבלתי קריאה מ-POST או GET!")
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
