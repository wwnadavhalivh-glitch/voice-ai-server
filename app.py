import os
from flask import Flask, request
from google import genai

app = Flask(__name__)

# שליפת מפתח ג'מיני שכבר הגדרת ברנדר
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "השרת פועל תקין!", 200

@app.route('/webhook', methods=['POST', 'GET'])
def handle_voice():
    # פקודת הקלטה מיוחדת של ימות המשיח (משמיעה צפצוף, מקליטה עד 60 שניות וממתינה לסולמית)
    yemot_record_command = "&read=voice_input=record,no,2,60,no,no,yes,no"

    # 1. בדיקה האם המשתמש סיים להקליט וימות המשיח שלחה את קובץ השמע
    if request.files:
        try:
            # לקיחת קובץ השמע שנשלח מהטלפון
            audio_file = next(iter(request.files.values()))
            audio_data = audio_file.read()
            
            # אתחול ג'מיני
            client = genai.Client(api_key=API_KEY)
            
            print("שולח את קובץ השמע לעיבוד בג'מיני...")
            # ג'מיני מקשיב לקובץ השמע ומבין את העברית בעצמו
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    {"mime_type": "audio/wav", "data": audio_data},
                    "תקשיב לקובץ השמע בעברית, ותענה על השאלה שנשאלה שם בצורה קצרה, ברורה ותמציתית."
                ]
            )
            
            ai_response = response.text.replace('*', '').replace('#', '').strip()
            print(f"תשובת ג'מיני: {ai_response}")
            
            # מחזיר את התשובה בטקסט (ימות המשיח תקריא) ומיד פותח שוב מיקרופון לשאלה הבאה (לולאה)
            return f"id_list_message=t-{ai_response}{yemot_record_command}"
            
        except Exception as e:
            print(f"שגיאה בעיבוד השמע בג'מיני: {e}")
            return f"id_list_message=t-התרחשה שגיאה בעיבוד הקול.{yemot_record_command}"

    # 2. אם זו תחילת השיחה ועדיין אין קובץ שמע - נשמיע פתיחה ונפעיל את הצפצוף וההקלטה
    return f"id_list_message=t-שלום. אנא הקלט את שאלתך לאחר הצליל, ובסיום לחץ סולמית.{yemot_record_command}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
