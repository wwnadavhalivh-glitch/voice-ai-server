import os
import requests
from flask import Flask, request, Response
from google import genai
from google.genai import types

app = Flask(__name__)

# אתחול ה-Client של ג'ימיני
client = genai.Client()

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice_endpoint():
    # ימות המשיח שולחים את נתיב הקובץ בפרמטר file_url
    audio_url = request.values.get('file_url', '')

    if not audio_url:
        print("\n=== פנייה ללא קובץ שמע ===")
        return Response("read=t=לא התקבל קובץ שמע=no,no,no&", mimetype='text/plain; charset=utf-8')

    print(f"\n=== התקבל קובץ שמע חדש: {audio_url} ===")
    
    try:
        # הורדת קובץ השמע לזיכרון השרת
        audio_response = requests.get(audio_url)
        audio_data = audio_response.content
        
        print("שולח לג'ימיני לעיבוד...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=audio_data,
                    mime_type='audio/wav'
                ),
                "הקשב לקובץ השמע וענה עליו בעברית בקצרות (עד 2 משפטים)."
            ]
        )
        
        answer_text = response.text
        print(f"תשובת ג'ימיני: {answer_text}")

        return Response(f"read=t={answer_text}=no,no,no&", mimetype='text/plain; charset=utf-8')

    except Exception as e:
        print(f"שגיאה בעיבוד השמע: {e}")
        return Response("read=t=חלה שגיאה זמנית במערכת=no,no,no&", mimetype='text/plain; charset=utf-8')

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def home_endpoint():
    # החזרת תגובה תקינה גם ל-HEAD וגם ל-GET כדי שרנדר ידע שהשרת חי ובריא ולא יכבה אותו!
    return Response("OK", status=200, mimetype='text/plain')

if __name__ == '__main__':
    # התאמה מלאה למערכת הפורטים של Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
