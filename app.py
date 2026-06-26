import os
import urllib.parse  # השורה החסרה שהפילה את השרת!
import urllib.parse
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
        # בדיקה שיש קובץ
        if not request.files:
            error_text = urllib.parse.quote("לא התקבל קובץ שמע.")
            return f"id_list_message=t-{error_text}"
            
        audio_file = next(iter(request.files.values()))
        audio_data = audio_file.read()
        
        # שליחה לג'מיני
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                {"mime_type": "audio/wav", "data": audio_data},
                "תקשיב לקובץ השמע בעברית, ותענה על השאלה שנשאלה שם בצורה קצרה, ברורה ותמציתית."
            ]
        )
        
        ai_response = response.text.replace('*', '').replace('#', '').strip()
        
        # קידוד התשובה לעברית (עכשיו זה יעבוד כי הוספנו את ה-import)
        encoded_response = urllib.parse.quote(ai_response)
        return f"id_list_message=t-{encoded_response}"
        
    except Exception as e:
        print(f"שגיאה בעיבוד הקול: {e}")
        error_text = urllib.parse.quote("התרחשה שגיאה בעיבוד הקול. אנא נסה שוב.")
        return f"id_list_message=t-{error_text}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
