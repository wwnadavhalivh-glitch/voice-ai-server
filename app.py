import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    
    # 1. בדיקה: האם הגענו לשלב שבו ימות המשיח סיימו להקליט ומביאים לנו את הקובץ?
    if 'UploadFile' in request.files:
        audio_file = request.files['UploadFile']
        
        # השרת לוקח את הקובץ ושומר אותו אצלו (על שרת ה-Render)
        audio_file.save("user_question.wav")
        print("הקובץ נשמר בהצלחה על שרת הרנדר!")
        
        # השרת שולח פקודה אחרונה: להגיד שהקובץ נשמר ולנתק
        return "read=t-הקובץ נשמר בהצלחה בשרת.&hangup"


    # 2. אם הגענו לכאן - סימן שהקובץ לא קיים, כלומר המשתמש הרגע נכנס לשלוחה!
    # השרת מיד שולח פקודה לימות המשיח מה לעשות:
    print("משתמש נכנס לשיחה - שולח פקודת הקלטה...")
    
    # הפקודה אומרת: תשמיעו לו את הטקסט, ותקליטו אותו עד שהוא יקיש סולמית
    return "read=t-אנא הקלט את הודעתך ובסיום הקש סולמית.&api_audio_record=yes"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
