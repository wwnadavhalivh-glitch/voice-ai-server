import os
from flask import Flask, request, Response

app = Flask(__name__)

# אם סתם נכנסים לקישור בדפדפן
@app.route('/', methods=['GET', 'POST'])
def home():
    return "השרת באוויר!"

# הכתובת שימות המשיח פונים אליה (לפי ה-ext.ini שלך)
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- ימות המשיח פנו לשרת בהצלחה! ---")
    
    # הפקודה שתגרום למערכת להקריא לך את המספרים 123
    פקודה_לימות_המשיח = "read=num-123"
    
    # מחזירים את הפקודה בפורמט text/plain שהמערכת דורשת
    return Response(פקודה_לימות_המשיח, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
