import os
from flask import Flask, request
from google import genai

app = Flask(__name__)

# שליפת מפתח ה-API שהגדרנו ב-Render
API_KEY = os.environ.get("GEMINI_API_KEY")
# אתחול הלקוח של ג'מיני באמצעות הספרייה החדשה
client = genai.Client(api_key=API_KEY) if API_KEY else None

@app.route('/', methods=['GET'])
def home():
    return "השרת של ג'מיני באוויר!", 200

@app.route('/webhook', methods=['POST', 'GET'])
def handle_voice():
    # ימות המשיח שולחת את הטקסט שנקלט תחת הפרמטר 'stt_text'
    user_text = request.args.get('stt_text', '')
    
    # הדפסה ללוגים בשבילך לראות מה האדם אמר
    print(f"המשתמש אמר בטלפון: {user_text}")
    
    if not user_text:
        # אם האדם עדיין לא דיבר או שהקריאה רק התחילה
        return "id_list_message=t-שלום, אני הבוט החכם שלך. אנא שאל את שאלתך לאחר הצליל.&&timeout=10"

    if not client:
        return "id_list_message=t-שגיאה, מפתח ה-API לא מוגדר בשרת."

    try:
        # שליחת השאלה למודל Gemini 2.5 Flash המהיר
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
        )
        ai_response = response.text
        
        # ניקוי תווים מיוחדים כמו כוכביות שהמודל לפעמים מחזיר, כדי שימות המשיח תקריא חלק
        ai_response = ai_response.replace('*', '').replace('#', '').strip()
        
        # החזרת התשובה לימות המשיח להקראה, והשארת הערוץ פתוח לשאלה הבאה
        return f"id_list_message=t-{ai_response}"
        
    except Exception as e:
        print(f"שגיאה בעיבוד מול ג'מיני: {e}")
        return "id_list_message=t-התרחשה שגיאה בעיבוד הנתונים."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
