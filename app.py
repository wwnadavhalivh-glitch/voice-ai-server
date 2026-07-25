import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- פנייה נכנסה משרת ימות המשיח ---")
    
    # שלב ב': המשתמש סיים להקליט והקובץ הגיע לשרת
    if 'UploadFile' in request.files:
        audio_file = request.files['UploadFile']
        
        # שמירת הקובץ בשרת
        file_path = "user_recording.wav"
        audio_file.save(file_path)
        print("קובץ השמע התקבל ונשמר בהצלחה בשרת!")
        
        # השמעת הודעת אישור מובנית של ימות המשיח (M1211 = "תודה רבה") וניתוק השיחה
        response_text = "play_and_get_audio=M1211&hangup=yes"
        return Response(response_text, mimetype='text/plain')

    # שלב א': כניסה ראשונית של המשתמש לשלוחה
    print("שולח פקודת הקלטה תקנית עם ביפ...")
    
    # פקודת API רשמית של ימות המשיח להקלטת קול עם ביפ מובנה:
    # read=f-M0000 מקריא את קובץ המערכת של ההקלטה
    # val_1_type=record מגדיר שזו הקלטה
    # record_beep=yes מפעיל את הצפצוף (ביפ) בתחילת ההקלטה!
    response_text = "read=f-M0000&val_1_type=record&record_beep=yes"
    return Response(response_text, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
