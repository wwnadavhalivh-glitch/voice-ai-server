import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice_endpoint():
    # שליפת הטקסט שימות המשיח ישלחו אלינו חזרה במשתנה ApiText
    user_text = request.values.get('ApiText', '').strip()
    
    print("\n" + "="*40)
    print(f"!!! הטקסט שנקלט מהטלפון: {user_text} !!!")
    print("="*40 + "\n")

    # פנייה ראשונה: המשתמש רק נכנס לשלוחה ועוד לא דיבר
    if not user_text:
        # פקודה רשמית: תקריא טקסט (t=), תפעיל המרת דיבור (api_text_convert=yes) ותחזיר למשתנה (var=ApiText)
        response_format = "read=t=נא לומר את שאלתך לאחר הצליל ובסיום לחץ סולמית&api_text_convert=yes&var=ApiText&"
        return Response(response_format, mimetype='text/plain; charset=utf-8')
    
    # פנייה שנייה: המשתמש דיבר והטקסט חזר לשרת בהצלחה!
    response_format = f"read=t=השרת קלט בהצלחה את מה שאמרת. אמרת: {user_text}&"
    return Response(response_format, mimetype='text/plain; charset=utf-8')

@app.route('/', methods=['GET', 'POST'])
def home_endpoint():
    return gemini_voice_endpoint()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
