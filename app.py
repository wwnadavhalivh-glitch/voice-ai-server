import time
import os
import gc
from flask import Flask, request, Response
from google import genai

app = Flask(__name__)

# הגדרת הלקוח של ג'מיני
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- קבלה פניה חדשה ממוקד הטלפוניה ---")
    print(f"Args (GET): {request.args.to_dict()}")

    # 1. חילוץ בטוח של הערך הקולי האחרון שהתקבל מכל משתנה מתאים
    text_values = [v for k, v in request.args.items() if k.startswith('text')]
    if text_values:
        raw_text = str(text_values[-1])
    else:
        args_list = list(request.args.values())
        raw_text = str(args_list[-1]) if args_list else ''

    user_text = raw_text.split(',')[-1].strip() if raw_text else None

    # 2. טיפול בפנייה המכילה שאלה מהמשתמש
    if user_text:
        print(f"=== הנתונים שהתקבלו מהמשתמש: {user_text} ===")
        
        # שליחת השאלה לג'מיני
        response = client.models.generate_content(
            model='models/gemini-3.5-flash',
            contents=f"ענה בעברית פשוטה ובלי סמלים מיוחדים, בלי נקודות, כוכביות או אנגלית, ותשיב רק פסיקים על השאלה הבאה: {user_text}"
        )
        
        # ניקוי ירידות שורה וגרשיים מהתשובה כדי למנוע תקלות בפענוח
        ai_answer = response.text.strip().replace('\n', ' ').replace('"', '').replace("'", '')
        print(f"=== התקבלה תשובה מג'מיני: {ai_answer} ===")

        # יצירת שם משתנה דינמי ייחודי המונע קונפליקטים בימות המשיח
        var_name = f"text_{int(time.time())}"
        
        # הרכבת פקודת ה-read הנקייה
        response_text = f"read=t-{ai_answer} כעת אנא הקלט את שאלתך הבאה לאחר הצליל ובסיום הקש סולמית={var_name},,voice"
        
        gc.collect()
        return Response(response_text, mimetype='text/plain; charset=utf-8')

    # 3. ברירת מחדל (פנייה ראשונה ללא טקסט)
    else:
        response_text = "read=t-שלום אנא הקלט את הודעתך לאחר הצליל ובסיום הקש סולמית=text,,voice"
        gc.collect()
        return Response(response_text, mimetype='text/plain; charset=utf-8')

@app.route('/')
def home():
    return Response("השרת פעיל", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
