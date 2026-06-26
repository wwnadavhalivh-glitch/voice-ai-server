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
    # בשלוחת הקלטה (type=record), ימות המשיח שולחים את קובץ השמע בפרמטר שנקרא 'file_url'
    audio_url = request.values.get('file_url', '')

    if not audio_url:
        print("\n=== התקבלה פנייה ללא קובץ שמע ===")
        return Response("read=t=לא התקבל קובץ שמע מהמערכת=no,no,no&", mimetype='text/plain; charset=utf-8')

    print(f"\n=== התקבל קובץ שמע חדש מההקלטה: {audio_url} ===")
    
    try:
        # 1. הורדת קובץ השמע מהשרת של ימות המשיח לזיכרון
        audio_response = requests.get(audio_url)
        audio_data = audio_response.content
        
        # 2. שליחת הקובץ ישירות לג'ימיני שיקשיב לו
        print("שולח את ה-Audio לג'ימיני...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=audio_data,
                    mime_type='audio/wav'
                ),
                "הקשב היטב לקובץ השמע בעברית וענה עליו בקצרה ובשפה ברורה (עד 2 משפטים), מתאים להקראה קולית בטלפון."
            ]
        )
        
        answer_text = response.text
        print(f"תשובת ג'ימיני שמתקבלת: {answer_text}")

        # 3. החזרת התשובה למשתמש (המערכת תקריא לו את הטקסט של ג'ימיני)
        response_format = f"read=t={answer_text}=no,no,no&"
        return Response(response_format, mimetype='text/plain; charset=utf-8')

    except Exception as e:
        print(f"שגיאה בתהליך עיבוד השמע: {e}")
        return Response("read=t=חלה שגיאה בעיבוד הנתונים באיי איי=no,no,no&", mimetype='text/plain; charset=utf-8')

@app.route('/', methods=['GET', 'POST'])
def home_endpoint():
    return "Server is running perfectly for Yemot Recorder!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
