import os
from flask import Flask, request, Response
import google.generativeai as genai

app = Flask(__name__)

# הגדרת מפתח ה-API של גוגל (מומלץ להגדיר כמשתנה סביבה Environment Variable ב-Render)
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_ACTUAL_API_KEY_HERE")
genai.configure(api_key=GOOGLE_API_KEY)

# בחירת המודל (למשל Gemini 1.5 Flash שהוא מהיר וזול)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice():
    # 1. קבלת הטקסט שהומר מהמערכת של ימות המשיח
    # ימות המשיח שולחים את זה בפרמטר שקבענו (ApiText)
    user_text = request.args.get('ApiText', '')
    
    # הגנה במקרה שהטקסט ריק או שהזיהוי נכשל
    if not user_text:
        # מחזירים פקודה לימות המשיח להקריא שלא נקלטה שאלה
        response_text = "read=t=לא שמעתי את השאלה, אנא נסה שנית.&"
        return Response(response_text, mimetype='text/plain')
    
    try:
        # הנחיה קצרה למודל כדי שהתשובות יהיו מתאימות להקראה טלפונית (בלי סימנים מוזרים, קצרות יחסית)
        system_instruction = "אתה עוזר קולי בטלפון. תענה בעברית, בצורה קצרה, ברורה ובלי להשתמש בסימני עיצוב של טקסט כמו כוכביות או נקודות של רשימות."
        
        # 2. שליחת השאלה ל-Gemini
        # הערה: בשביל שיחה זורמת עם זיכרון בעתיד נשתמש ב-chat, כרגע זה פשוט שאלה-תשובה
        gemini_response = model.generate_content(
            f"{system_instruction}\n\nהשאלה של המשתמש: {user_text}"
        )
        
        answer = gemini_response.text
        
        # ניקוי בסיסי של תווים שעלולים לבלבל את מנוע הדיבור (כמו כוכביות שגוגל אוהב להחזיר)
        answer = answer.replace('*', '').replace('#', '').strip()
        
        # 3. יצירת התשובה בפורמט של ימות המשיח
        # הפקודה read=t= אומרת למערכת להקריא את הטקסט הבא (TTS)
        # בסוף נשים תו & כפי שנדרש בפרוטוקול שלהם
        response_text = f"read=t={answer}&"
        
    except Exception as e:
        print(f"Error: {e}")
        response_text = "read=t=מתנצל, אירעה שגיאה בעיבוד השאלה שלך.&"
    
    # החזרת התשובה כטקסט פשוט (text/plain) עם קידוד utf-8 כדי שהעברית לא תתבשבש
    return Response(response_text, mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    # Render דורשת להאזין לפורט שהיא מגדירה במשתנה הסביבה PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
