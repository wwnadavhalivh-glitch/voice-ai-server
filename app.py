import os
from flask import Flask, request, Response
import google.generativeai as genai

app = Flask(__name__)

# הגדרת מפתח ה-API
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# מודל Gemini 1.5 Flash - מהיר ומצוין
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/gemini-voice', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def gemini_voice():
    # שליפת הטקסט שימות המשיח תרגמו מהקול של המשתמש
    user_text = request.args.get('ApiText', '').strip()
    
    # הדפסה ללוג של רנדר כדי שתוכל לראות מה המשתמש אמר
    print(f"User asked: {user_text}")

    # אם המשתמש לא אמר כלום או שהתרגום ריק
    if not user_text:
        return Response("read=t=לא שמעתי או לא הבנתי את השאלה, אנא נסה שוב.&", mimetype='text/plain; charset=utf-8')

    try:
        # הנחיית מערכת ל-Gemini
        system_instruction = "אתה עוזר קולי בטלפון. תענה בעברית, בצורה קצרה (עד 2-3 משפטים), ברורה ובלי להשתמש בסימני עיצוב של טקסט כמו כוכביות או סולמיות."
        
        # פנייה ל-Gemini
        gemini_response = model.generate_content(f"{system_instruction}\n\nהשאלה: {user_text}")
        answer = gemini_response.text
        
        # ניקוי תווים מיוחדים ליתר ביטחון
        answer = answer.replace('*', '').replace('#', '').replace('\n', ' ').strip()
        
        print(f"Gemini answered: {answer}")
        
        # החזרת הפקודה לימות המשיח
        response_text = f"read=t={answer}&"
        return Response(response_text, mimetype='text/plain; charset=utf-8')

    except Exception as e:
        print(f"Error: {e}")
        return Response("read=t=מתנצל, אירעה שגיאה בקבלת התשובה מג'מיני.&", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
