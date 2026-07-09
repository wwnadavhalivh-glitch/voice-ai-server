import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK - השרת באוויר ומנהל את שיחת הטלפון!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- פנייה חדשה נכנסה לשרת מימות המשיח ---")
    
    # שלב ד': בדיקה האם המשתמש כבר הקליט והקובץ חזר אלינו
    if 'UploadFile' in request.files:
        audio_file = request.files['UploadFile']
        print(f"הקלטה התקבלה! שם זמני: {audio_file.filename}")
        
        # שמירת הקובץ על השרת ברנדר
        audio_file.save("user_question.wav")
        print("הקובץ נשמר בהצלחה בשרת.")
        
        # הודעה מהשרת שהקובץ נשמר בהצלחה וניתוק
        return "read=t-הקובץ נשמר בהצלחה בשרת.&hangup"
        
    # שלב ב': המשתמש רק נכנס לשלוחה (אין עדיין קובץ בבקשה)
    # השרת אומר לימות המשיח להשמיע פקודה, להקליט, ולחזור אליו בסיום בסולמית
    print("המחייג נכנס לשלוחה. שולח פקודת הקלטה...")
    
    # הפקודה אומרת: תשמיע טקסט (t-אנא הקלט...), ותפעיל הקלטה (api_audio_record=yes)
    return "read=t-אנא הקלט את הודעתך ובסיום הקש סולמית.&api_audio_record=yes"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
