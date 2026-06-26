import os
import urllib.parse
from flask import Flask, request
from google import genai

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_API_KEY")

# הכל קורה עכשיו בנתיב הראשי של השרת
@app.route('/', methods=['POST', 'GET'])
def handle_voice():
    recording_settings = ",record,no,2,60,no,no,yes,no"

    # א. אם זו פנייה ראשונה ואין קובץ - משמיעים פתיח ומקליטים
    if not request.files:
        text_to_say = "שלום. אנא שאל את שאלתך לאחר הצליל, ובסיום לחץ סולמית."
        encoded_text = urllib.parse.quote(text_to_say)
        return f"read=t-{encoded_text}=voice_input{recording_settings}"

    # ב + ג. אם הגיע קובץ שמע - מעבדים בג'מיני
    try:
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
        
        # ד. מחזירים את התשובה המקודדת להקראה
        encoded_response = urllib.parse.quote(ai_response)
        return f"id_list_message=t-{encoded_response}"
        
    except Exception as e:
        print(f"Error: {e}")
        error_text = urllib.parse.quote("התרחשה שגיאה בעיבוד הקול.")
        return f"id_list_message=t-{error_text}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
