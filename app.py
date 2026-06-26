import os
import requests
import asyncio
from flask import Flask, request, Response
from google import genai
from google.genai import types
import edge_tts

app = Flask(__name__)

# אתחול ה-Client של ג'ימיני (יושב על ה-API KEY הקיים שלך במערכת)
client = genai.Client()

async def generate_speech_file(text, output_path):
    """פונקציה שהופכת טקסט לקובץ דיבור בעברית"""
    communicate = edge_tts.Communicate(text, "he-IL-AvriNeural")
    await communicate.save(output_path)

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice_endpoint():
    # ימות המשיח שולחים לנו את הנתיב לקובץ שהוקלט בפרמטר api_url
    audio_url = request.values.get('api_url', '')

    # פנייה ראשונה של השיחה (עדיין אין קובץ מוקלט)
    if not audio_url:
        print("\n=== פנייה ראשונה: מפעיל הקלטה ===")
        # מחזיר פקודה ריקה, מה שיגרום לימות המשיח להפעיל את ה-record שהגדרנו ב-ext.ini
        return Response("play_and_get_input=", mimetype='text/plain; charset=utf-8')

    print(f"\n=== התקבל קובץ שמע מימות המשיח: {audio_url} ===")
    
    try:
        # 1. הורדת קובץ השמע מימות המשיח לזיכרון של השרת
        audio_response = requests.get(audio_url)
        audio_data = audio_response.content
        
        # 2. שליחת קובץ השמע ישירות לג'ימיני
        print("שולח את ה-Audio לג'ימיני...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=audio_data,
                    mime_type='audio/wav'
                ),
                "הקשב היטב לקובץ השמע בעברית וענה עליו בקצרה ובשפה ברורה (משפט אחד או שניים), מתאים להקראה בטלפון."
            ]
        )
        
        answer_text = response.text
        print(f"תשובת ג'ימיני: {answer_text}")

        # 3. יצירת קובץ דיבור מהתשובה של ג'ימיני
        # (בינתיים נחזיר להם את זה כטקסט שהמערכת שלהם תקרא, בשביל הניסוי הראשוני שלא יסתבך)
        response_format = f"read=t={answer_text}=no,no,no&"
        return Response(response_format, mimetype='text/plain; charset=utf-8')

    except Exception as e:
        print(f"שגיאה בתהליך: {e}")
        return Response("read=t=חלה שגיאה בעיבוד הנתונים&", mimetype='text/plain; charset=utf-8')

@app.route('/', methods=['GET', 'POST'])
def home_endpoint():
    return gemini_voice_endpoint()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
