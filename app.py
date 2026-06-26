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
    # פקודת rapi,,record שולחת את הקישור באחד משני הפרמטרים הבאים:
    audio_url = request.values.get('recording_file_link') or request.values.get('file_url', '')

    if not audio_url:
        print("\n=== פנייה ראשונית או ללא קובץ שמע ===")
        return Response("", mimetype='text/plain; charset=utf-8')

    print(f"\n=== ג. הקובץ אושר ונשלח לשרת! הקישור: {audio_url} ===")
    
    try:
        # הורדת קובץ השמע
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
        print(f"ד. תשובת ג'ימיני המוכנה: {answer_text}")

        # השמעת התשובה למשתמש בטלפון
        return Response(f"read=t={answer_text}=no,no,no&", mimetype='text/plain; charset=utf-8')

    except Exception as e:
        print(f"שגיאה בעיבוד השמע: {e}")
        return Response("read=t=חלה שגיאה בעיבוד התשובה=no,no,no&", mimetype='text/plain; charset=utf-8')

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def home_endpoint():
    return Response("OK", status=200, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
