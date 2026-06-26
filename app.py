import os
from flask import Flask, request
from google import genai

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "השרת פועל וממתין לשיחות!", 200


@app.route('/webhook', methods=['POST', 'GET'])
def handle_voice():
    # הגדרות הזמן והצליל של ההקלטה (לפי חוקי ימות המשיח)
    # 2 = מינימום שניות | 60 = מקסימום שניות | yes = השמעת צפצוף להתחלת הקלטה
    recording_settings = ",record,no,2,60,no,no,yes,no"

    # ====================================================
    # א. הודעה ראשונית של "אנא שאל" + הפעלת צליל והקלטה
    # ====================================================
    # אם המשתמש רק נכנס לשלוחה בטלפון ועדיין לא נשלח קובץ שמע לשרת
    if not request.files:
        return f"read=t-שלום. אנא שאל את שאלתך לאחר הצליל, ובסיום לחץ סולמית.=voice_input{recording_settings}"

    # ====================================================
    # ב + ג. אישור המפתח של ג'מיני ושליחת קובץ השמע לשרת
    # ====================================================
    # בלוק זה יתבצע אך ורק אחרי שהמשתמש סיים לדבר ויש קובץ שמע מוכן בשרת
    try:
        # תפיסת קובץ השמע שהגיע מימות המשיח
        audio_file = next(iter(request.files.values()))
        audio_data = audio_file.read()
        
        # התחברות לג'מיני באמצעות המפתח
        client = genai.Client(api_key=API_KEY)
        
        # שליחת הקובץ הדיגיטלי לג'מיני לקבלת תשובה
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                {"mime_type": "audio/wav", "data": audio_data},
                "תקשיב לקובץ השמע בעברית, ותענה על השאלה שנשאלה שם בצורה קצרה, ברורה ותמציתית."
            ]
        )
        
        # ניקוי תווים מיוחדים מהתשובה הכתובה שחזרה
        ai_response = response.text.replace('*', '').replace('#', '').strip()
        
        # ====================================================
        # ד. הטקסט שחזר - להשמיע אותו בימות המשיח (וזהו)
        # ====================================================
        # פקודה זו משמיעה למחייג את תשובת הבוט ומסיימת את הפעולה, בלי לפתוח הקלטה נוספת
        return f"id_list_message=t-{ai_response}"
        
    except Exception as e:
        print(f"שגיאה בעיבוד הקול: {e}")
        return "id_list_message=t-התרחשה שגיאה זמנית בעיבוד הקול. אנא נסה שוב מאוחר יותר."


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
