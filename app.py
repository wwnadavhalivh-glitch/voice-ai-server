import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- פנייה התקבלה מהמערכת ---")
    
    # מקרה 1: המשתמש סיים להקליט והקובץ הגיע לשרת
    if 'UploadFile' in request.files:
        audio_file = request.files['UploadFile']
        audio_file.save("user_recording.wav")
        print("קובץ השמע התקבל ונשמר בהצלחה!")
        
        # השמעת הודעת תודה וניתוק
        return Response("play_and_get_audio=M1211&hangup=yes", mimetype='text/plain')

    # מקרה 2: כניסה ראשונית - עדיין אין קובץ, לכן מורים למערכת להקליט
    print("שולח פקודת הקלטה מובנית לשרת ימות המשיח...")
    
    # api_add_audio_record=yes מורה למערכת להשמיע את הודעת ההקלטה M0000,
    # להשמיע ביפ, לקלוט הקלטה, ורק כשהמשתמש מקיש # לשלוח אותה בחזרה ל-API.
    response_text = "api_add_audio_record=yes"
    return Response(response_text, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
