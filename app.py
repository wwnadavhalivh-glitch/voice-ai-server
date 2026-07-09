import os
from flask import Flask, request

app = Flask(__name__)

# נתיב ה-webhook שימות המשיח מחייגים אליו
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- פנייה חדשה נכנסה משלוחה 2! ---")
    
    # הבדיקה הבסיסית: אם מגיע קובץ, נשמור אותו
    if 'UploadFile' in request.files:
        audio_file = request.files['UploadFile']
        audio_file.save("user_voice.wav")
        print("הקובץ נשמר בהצלחה בשרת!")
        return "read=t-ההקלטה נקלטה בהצלחה בשרת.&hangup=yes"

    # אם זו כניסה ראשונית (כמו הפעם ההיא שזה עבד!)
    # אנחנו מחזירים טקסט נקי, עם ה-f כדי למנוע בעיות קידוד בעברית
    print("שולח פקודת הקלטה למערכת...")
    return f"read=t-אנא הקלט את הודעתך בצורה ברורה ובסיום הקש סולמית.&api_audio_record=yes"

# נתיב ראשי לגיבוי
@app.route('/', methods=['GET', 'POST'])
def home():
    return "השרת של רנדר חובר בהצלחה"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
