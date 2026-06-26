import os
from flask import Flask, request, Response

app = Flask(__name__)

def handle_voice_logic():
    # קריאת הטקסט שהגיע מימות המשיח
    user_text = request.values.get('ApiText', '').strip()
    
    print("\n" + "="*40)
    print(f"!!! הטקסט שנקלט מהטלפון: {user_text} !!!")
    print("="*40 + "\n")

    # פנייה ראשונה: המשתמש רק נכנס לשלוחה ועדיין לא דיבר
    if not user_text:
        # הפקודה הרשמית של ימות המשיח להקראת טקסט לפני תחילת ההקלטה של ה-API
        # s=הקלטת טקסט, t=טקסט להקראה, var=שם המשתנה שיחזור אלינו
        response_format = "read=f=s&t=אנא שאל את שאלתך לאחר הצליל ולחץ סולמית&var=ApiText&"
        return Response(response_format, mimetype='text/plain; charset=utf-8')
    
    # פנייה שנייה: המשתמש כבר דיבר ויש לנו טקסט!
    response_format = f"read=t=השרת קלט בהצלחה את מה שאמרת: {user_text}&"
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
