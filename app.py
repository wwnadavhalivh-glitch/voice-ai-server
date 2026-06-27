import os
from flask import Flask, request

app = Flask(__name__)

# נתיב ראשי לבדיקה שהשרת בכלל באוויר
@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK - Server is Running"

# הנתיב שאליו ימות המשיח ישלחו את קובץ ההקלטה
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print(f"התקבלה פנייה בשרת! סוג הבקשה: {request.method}")
    print(f"הפרמטרים שהתקבלו ב-Query: {request.args}")
    
    # בדיקה האם ימות המשיח שלחו קובץ
    if 'file' in request.files:
        audio_file = request.files['file']
        print(f"התקבל קובץ בהצלחה! שם הקובץ: {audio_file.filename}")
        
        # שמירת הקובץ בשרת בשם זמני כדי לוודא שהוא אכן מגיע
        audio_file.save("test_recording.wav")
        print("הקובץ נשמר בהצלחה בשרת.")
        
        # נחזיר פקודה פשוטה לנתק את השיחה, בלי לעבור לשום שלוחה
        return "read=t-הקובץ נקלט בשרת בהצלחה.&hangup"
    
    print("לא נמצא קובץ תחת השם file בבקשה.")
    return "read=t-השרת פועל אך לא נשלח קובץ שמע.&hangup"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
