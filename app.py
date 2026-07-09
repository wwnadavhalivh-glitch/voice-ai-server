import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK - השרת באוויר וממתין לקובץ האודיו"

@app.route('/webhook', methods=['POST'])
def webhook():
    print("--- פנייה חדשה נכנסה משלוחת API! ---")
    
    # בדיקה האם קיבלנו קובץ (בשלוחת API השם הוא 'UploadFile')
    if 'UploadFile' in request.files:
        audio_file = request.files['UploadFile']
        print(f"קובץ אודיו נקלט בהצלחה! שם זמני: {audio_file.filename}")
        
        # שמירת הקובץ בשרת ברנדר לבדיקה שהכל עבר
        audio_file.save("incoming_voice.wav")
        print("הקובץ נשמר בהצלחה על שרת הרנדר.")
        
        # הודעה למחייג שהקובץ הגיע בהצלחה וניתוק השיחה
        return "read=t-הקובץ התקבל בהצלחה בשרת.&hangup"
        
    print("אזהרה: התקבלה פנייה מה-API, אך לא נמצא קובץ בשדה UploadFile")
    return "read=t-השרת קיבל פנייה אך ללא קובץ שמע.&hangup"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
