import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK - Server is Up and Running!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- פנייה חדשה נכנסה ל-Webhook! ---")
    print(f"מתודה: {request.method}")
    
    # בדיקה האם הגיע קובץ
    if 'file' in request.files:
        file = request.files['file']
        print(f"קובץ נקלט בהצלחה! שם הקובץ במקור: {file.filename}")
        
        # שמירה מקומית בשרת לבדיקה
        file.save("uploaded_audio.wav")
        print("הקובץ נשמר בהצלחה על השרת ברנדר.")
        
        return "read=t-הקובץ נשלח ונקלט בשרת בהצלחה.&hangup"
        
    print("אזהרה: פנייה הגיעה אך לא נמצא קובץ בתוך השדה 'file'")
    return "read=t-הגעת לשרת בהצלחה, אך לא נשלח קובץ שמע.&hangup"

if __name__ == '__main__':
    # שינוי קריטי עבור Render - שימוש בפורט 10000 כברירת מחדל
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
