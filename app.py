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
    # שליחת הקישור באחד משני הפרמטרים שמתקבלים מימות המשיח בפנייה השנייה
    audio_url = request.values.get('recording_file_link') or request.values.get('file_url') or ''

    # בדיקה האם זו פנייה ראשונית (כשעדיין אין קובץ שמע)
    if not audio_url:
        print("\n=== פנייה ראשונית: שולח הוראת הקלטה לטלפון ===")
        instructions = (
            "api_000=rapi,,say_text,נא לומר את שאלתך לאחר הצליל ובסיום לחץ סולמית או המתן&"
            "api_001=rapi,,play_sound,beep&"
            "api_002=rapi,,record,/gemini_temp/auto,,yes,3,1&"
        )
        return Response(instructions, mimetype='text/plain; charset=utf-8')

    print(f"\n=== התקבל קישור לקובץ השמע: {audio_url} ===")

    try:
        # הורדת קובץ השמע מהשרת של ימות המשיח
        audio_response = requests.get(audio_url)
        audio_data = audio_response.content

        print("...שולח לג'ימיני לעיבוד...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=audio_data,
                    mime_type='audio/wav'
                ),
                ".הקשב לקובץ השמע וענה עליו בעברית בקצרות (עד 2 משפטים)"
            ]
        )

        answer_text = response.text
        print(f" תשובת ג'ימיני המוכנה: {answer_text}")

        # השמעת התשובה למשתמש בטלפון
        return Response(f"read=t={answer_text}=no,no,no&", mimetype='text/plain; charset=utf-8')

    except Exception as e:
        print(f" שגיאה בעיבוד השמע: {e}")
        return Response("read=t=חלה שגיאה בעיבוד התשובה=no,no,no&", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    # התאמה לפורט שרנדר מחייב (10000)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
