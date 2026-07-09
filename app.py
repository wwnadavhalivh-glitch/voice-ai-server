import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # פקודה בסיסית ביותר: רק להקריא מספר 123 ולנתק
    # הגודל של הטקסט הזה באנגלית הוא קטן מאוד ולא יכול להתפרש לא נכון
    return "read=num-123"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
