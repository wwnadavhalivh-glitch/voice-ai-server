import os
from flask import Flask, request
from google import genai

app = Flask(__name__)

# הגדרה מפורשת של המפתח מתוך משתני הסביבה של Render
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "השרת פועל!", 200

@app.route('/webhook', methods=['POST', 'GET'])
def handle_voice():
    # שליפת הטקסט שימות המשיח תרגמה מהדיבור של הלקוח
    user_text = request.args.get('stt_text', '')
    print(f"התקבל טקסט מהטלפון: {user_text}")
    
    # 1. בדיקה אם המפתח קיים בשרת
    if not API_KEY:
        print("שגיאה: מפתח GEMINI_API_KEY לא נמצא בשרת!")
        return "id_list_message=t-שגיאה. מפתח הגישה לא מוגדר בשרת הרנדר."

    # 2. אם השיחה רק התחילה ואין עדיין טקסט - נבקש מהמשתמש לדבר
    if not user_text:
        # הפקודה read_stt=yes אומרת לימות המשיח להפעיל את המיקרופון מיד לאחר השמעת המשפט
        return "id_list_message=t-שלום, אנא שאל את שאלתך לאחר הצליל.&&read_stt=yes"

    # 3. שליחת הטקסט ל-Gemini
    try:
        # אתחול הלקוח ישירות בתוך הפונקציה עם המפתח הקיים
        client = genai.Client(api_key=API_KEY)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
        )
        
        ai_response = response.text.replace('*', '').replace('#', '').strip()
        print(f"תשובת ג'מיני: {ai_response}")
        
        # החזרת התשובה ובקשה לשאלה נוספת (השארת הערוץ פתוח בלולאה)
        return f"id_list_message=t-{ai_response}&&read_stt=yes"
        
    except Exception as e:
        print(f"שגיאה בעיבוד מול ג'מיני: {e}")
        return "id_list_message=t-התרחשה שגיאה בתקשורת עם הבינה המלאכותית."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
