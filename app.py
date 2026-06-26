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
    print(f"התקבלה פנייה משלוחת הקלטה. קבצים: {list(request.files.keys())}. פרמטרים: {dict(request.values)}")

    # בשלוחת הקלטה, ימות המשיח שולחים את הקובץ עצמו בתוך request.files תחת השם 'file'
    if 'file' in request.files:
        print("נמצא קובץ שמע שנשלח ישירות מהטלפון!")
        audio_file = request.files['file']
        audio_data = audio_file.read()
    else:
        # גיבוי במידה והם שלחו כקישור (לפי הגדרות ישנות)
        audio_url = request.values.get('recording_file_link') or request.values.get('file_url') or ''
        if not audio_url:
            print("\n=== שגיאה: לא נמצא קובץ שמע בפנייה ===")
            return Response("read=t=לא התקבל קובץ שמע תקין במערכת=no,no,no&", mimetype='text/plain; charset=utf-8')
        
        print(f"מוריד קובץ שמע מהקישור: {audio_url}")
        import requests
        audio_data = requests.get(audio_url).content   audio_data = audio_response.content
        
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
