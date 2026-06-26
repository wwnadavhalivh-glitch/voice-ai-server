import os
from flask import Flask, request, Response

app = Flask(__name__)

def handle_voice_logic():
    # שליפת הטקסט שימות המשיח תרגמו מהקול שלך
    user_text = request.values.get('ApiText', '').strip()
    
    print("\n" + "="*40)
    print(f"!!! הטקסט שנקלט מהטלפון: {user_text} !!!")
    print("="*40 + "\n")

    # אם המשתמש הגיע לשלוחה בפעם הראשונה (לפני שהוא דיבר)
    if not user_text:
        # נחזיר הודעה ריקה בפורמט תקני, כדי שהמערכת של ימות המשיח תמשיך מיד להקלטה
       return Response("read=t=נא לדבר לאחר הצליל=ApiText", mimetype='text/plain; charset=utf-8')
    
    # אם המשתמש כבר דיבר והגיע טקסט - נחזיר פקודת הקראה תקנית ב-100%
    response_format = f"read=t=הצלחה! השרת קלט שאמרת: {user_text}&"
    return Response(response_format, mimetype='text/plain; charset=utf-8')

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice_endpoint():
    return handle_voice_logic()

@app.route('/', methods=['GET', 'POST'])
def home_endpoint():
    return handle_voice_logic()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
