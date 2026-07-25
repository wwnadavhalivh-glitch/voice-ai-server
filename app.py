import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- פנייה חדשה התקבלה מהקו ---")
    
    # שלב ב': המשתמש סיים להקליט והקובץ הגיע לשרת
    if 'UploadFile' in request.files:
        audio_file = request.files['UploadFile']
        
        # שמירת הקובץ המוקלט
        file_path = "user_recording.wav"
        audio_file.save(file_path)
        print("הקובץ נשמר בשרת בהצלחה!")
        
        # כאן מתבצע עיבוד/תמלול הקובץ...
        
        # החזרת הודעת אישור קולית וניתוק
        response_text = "read=t-הטקסט נשלח בהצלחה.&hangup=yes"
        return Response(response_text, mimetype='text/plain')

    # שלב א': כניסה ראשונית של המשתמש לשלוחה
    print("שולח פקודת השמעה + ביפ להקלטה...")
    
    # b-1 מוסיף את הצפצוף (ביפ) בתחילת ההקלטה
    # M0000 הוא קובץ המערכת: "אנא הקלט את הודעתך..."
    response_text = "play_and_get_audio=M0000.b-1"
    return Response(response_text, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
