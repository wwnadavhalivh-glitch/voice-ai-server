import os
from flask import Flask, request
from google import genai

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "השרת פועל וממתין לקבצים!", 200

@app.route('/webhook', methods=['POST'])
def handle_voice():
    try:
        # 1. ימות המשיח שלחה את הקובץ? תופסים אותו
        audio_file = next(iter(request.files.values()))
        audio_data = audio_file.read()
        
        # 2. שולחים לג'מיני לקבלת תשובה טקסטואלית
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                {"mime_type": "audio/wav", "data": audio_data},
                "תקשיב לקובץ השמע בעברית, ותענה על השאלה שנשאלה שם בצורה קצרה, ברורה ותמציתית."
            ]
        )
        
        # 3. מנקים תווים מיוחדים
        ai_response = response.text.replace('*', '').replace('#', '').strip()
        
        # 4. מחזירים טקסט נקי. ימות המשיח תקרא את זה ותקריא למשתמש אוטומטית!
        return f"id_list_message=t-{ai_response}"
        
    except Exception as e:
        print(f"שגיאה: {e}")
        return "id_list_message=t-התרחשה שגיאה בעיבוד השאלה שלך."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
