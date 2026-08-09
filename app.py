import gc
import os
from flask import Flask, Response, request
from google import genai
app = Flask(__name__)
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY_1") or os.environ.get("GEMINI_API_KEY_2")
client = genai.Client(api_key=api_key)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- קבלה פניה חדשה ממוקד הטלפוניה ---")
    print(f"Args (GET): {request.args.to_dict()}")
    
    # בדיקה האם הגיעו נתונים מהמשתמש (הטקסט שהוקלט והומר)
    raw_text = request.args.get('text', '')
    user_text = raw_text.split(',')[-1].strip() if raw_text else None
    if user_text:
        print(f"=== הנתונים שהתקבלו מהמשתמש: {user_text} ===")

       
        # שליחת הטקסט לג'מיני
        response = client.models.generate_content(
            model='models/gemini-3.5-flash',
            contents=f"ענה בעברית פשוטה ובלי סמלים מיוחדים, וגם בלי נקודות, כוכביות או אנגלית, ותוסיף רק פסיקים על השאלה הבאה: {user_text}",
            
        )
        ai_answer = response.text.strip().replace('\n', ' ')
        print(f"=== התקבלה תשובה מג'מיני: {ai_answer} ===")
        response_text = f"id_list_message=t-{ai_answer}&read=t-כעת, האם תרצה לשאול שאלה נוספת? אנא הקלט לאחר הצליל ובסיום הקש סולמית=text,,voice,60,10,1,10,no,yes,yes,no"
        gc.collect()
        
        return Response(response_text, mimetype='text/plain; charset=utf-8')
        
    else:
    # שליחת הפקודות מופרדות בירידת שורה (\n):
    # 1. השמעת הטקסט בפורמט t-
    # 2. מעבר מידי לפקודת הקלטה וקליטת טקסט מהמשתמש
        response_text = "read=t-שלום, אנא הקלט את הודעתך לאחר הצליל ובסיום הקש סולמית=text,,voice,max_time=60,timeout=10,no_say_recording=yes"
        gc.collect()
        return Response(response_text, mimetype='text/plain; charset=utf-8')

@app.route('/')
def home():
    return Response("השרת פעיל", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
