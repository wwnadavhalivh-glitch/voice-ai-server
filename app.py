import os
from flask import Flask, request, Response
import google.generativeai as genai
import requests

app = Flask(__name__)

# הגדרת מפתח ה-API
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# מודל 1.5 פלאש תומך מצוין בקבצי אודיו ישירות
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/gemini-voice', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def gemini_voice():
    # ימות המשיח שולחים את נתיב קובץ השמע המוקלט בפרמטר המערכת
    # בדרך כלל בקובץ הקלטה הפרמטר נקרא למשל 'ApiFileUrl' או שהוא מורד ישירות
    # לצורך פשטות ואמינות מוחלטת, נבדוק אם יש טקסט או קובץ:
    
    file_url = request.args.get('ApiFileUrl', '') or request.args.get('url', '')
    user_text = request.args.get('ApiText', '')

    # הנחיית מערכת קבועה לבוט
    system_instruction = "אתה עוזר קולי בטלפון. תענה בעברית, בצורה קצרה, ברורה ובלי להשתמש בסימני עיצוב של טקסט כמו כוכביות."

    try:
        # אפשרות א': קיבלנו קובץ אודיו ישיר
        if file_url:
            # הורדת קובץ האודיו זמנית לשרת
            audio_data = requests.get(file_url).content
            audio_path = "user_audio.wav"
            with open(audio_path, "wb") as f:
                f.write(audio_data)
            
            # העלאת הקובץ ל-API של Gemini
            audio_file = genai.upload_file(path=audio_path)
            
            # בקשת תשובה מהמודל המבוססת על האודיו
            gemini_response = model.generate_content([
                system_instruction,
                "הקשב לקובץ השמע המצורף וענה עליו בקצרה ובעברית:",
                audio_file
            ])
            
            # ניקוי הקובץ הזמני
            if os.path.exists(audio_path):
                os.remove(audio_path)
                
            answer = gemini_response.text

        # אפשרות ב': גיבוי למקרה שהגיע כטקסט מהמערכת
        elif user_text:
            gemini_response = model.generate_content(f"{system_instruction}\n\nהשאלה: {user_text}")
            answer = gemini_response.text
            
        else:
            # אם הגעת לכאן ואין עדיין קובץ, נבקש מהמשתמש לדבר
            return Response("read=t=אנא הקלט את שאלתך לאחר הצליל ולחץ סולמית.&", mimetype='text/plain; charset=utf-8')

        # ניקוי סימני עיצוב מהטקסט של גוגל
        answer = answer.replace('*', '').replace('#', '').strip()
        
        # החזרת הפקודה לימות המשיח להקראת התשובה
        response_text = f"read=t={answer}&"
        return Response(response_text, mimetype='text/plain; charset=utf-8')

    except Exception as e:
        print(f"Error occurred: {e}")
        return Response("read=t=מתנצל, אירעה שגיאה בעיבוד השמע שלך.&", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
