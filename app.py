import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- שיחה נכנסה: שולח פקודת בדיקה עם Content-Type תקין ---")
    
    פקודה = "read=num-123"
    
    # יצירת תגובה מיוחדת שמכריחה את ימות המשיח להבין את הטקסט
    return Response(פקודה, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
