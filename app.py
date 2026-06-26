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
    # שורת ההקלטה הרשמית של ימות המשיח באמצעות פקודת read
    # היא מקריאה טקסט, מקליטה קובץ בשם voice_input וממתינה עד 60 שניות או סולמית
    yemot_record_command = "read=t-שלום. אנא שאל את שאלתך לאחר הצליל, ובסיום לחץ סולמית.=voice_input,record,no,2,60,no,no,yes,no"

    # ====================================================
    # 1. בדיקה: אם לא הגיע שום קובץ שמע בבקשה
    # ====================================================
    if not request.files:
        # במקום לקרוס, פשוט נשמיע למשתמש את הודעת הפתיחה וההקלטה
        return yemot_record_command

    # ====================================================
    # 2. אם הגענו לכאן - סימן שיש קובץ שמע! מעבדים בג'מיני
    # ====================================================
    try:
        # לקיחת קובץ השמע שנשלח מהטלפון
        audio_file = next(iter(request.files.values()))
        audio_data = audio_file.read()
        
        client = genai.Client(api_key=API_KEY)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                {"mime_type": "audio/wav", "data": audio_data},
                "תקשיב לקובץ השמע בעברית, ותענה על השאלה שנשאלה שם בצורה קצרה, ברורה ותמציתית."
            ]
        )
        
        ai_response = response.text.replace('*', '').replace('#', '').strip()
        
        # החזרת התשובה של ג'מיני להקראה בטלפון
        return f"id_list_message=t-{ai_response}"
        
    except Exception as e:
        print(f"שגיאה בעיבוד הקול: {e}")
        # אם יש שגיאה אמיתית מול ג'מיני, נשמיע הודעה ונפתח שוב הקלטה
        return f"id_list_message=t-התרחשה שגיאה בעיבוד הקול.&{yemot_record_command}"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
