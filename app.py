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
    
    # ====================================================
    # א. פנייה ראשונה (GET) - משמיע הודעה ופותח הקלטה
    # ====================================================
    if request.method == 'GET':
        # t- קורא את הטקסט. f- הפקודה הרשמית של ימות המשיח להקלטת קובץ (voice_input)
        return "id_list_message=t-שלום. אנא שאל את שאלתך לאחר הצליל, ובסיום לחץ סולמית.&חשבון=f-voice_input"

    # ====================================================
    # ב + ג. קבלת קובץ השמע (POST) ועיבוד בג'מיני
    # ====================================================
    try:
        # תפיסת קובץ השמע שנשלח מהטלפון
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
        
        # ====================================================
        # ד. השמעת התשובה שחזרה למשתמש
        # ====================================================
        return f"id_list_message=t-{ai_response}"
        
    except Exception as e:
        print(f"שגיאה בעיבוד הקול: {e}")
        return "id_list_message=t-התרחשה שגיאה בעיבוד הקול. אנא נסה שוב."


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
