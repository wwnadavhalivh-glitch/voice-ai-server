import os
from flask import Flask, request, Response

app = Flask(__name__)

def handle_voice_logic():
    # קריאת הטקסט שהגיע מהטלפון
    user_text = request.values.get('ApiText', '').strip()
    
    print("\n" + "="*40)
    print(f"!!! הטקסט שהתקבל מהטלפון: {user_text} !!!")
    print("="*40 + "\n")

    # אם זו תחילת השיחה והטקסט ריק - נחזיר פקודה שמפעילה את מנוע ההקלטה של ימות המשיח!
    if not user_text:
        # הפקודה הזו אומרת למערכת: תשמיעי צפצוף, תתחילי להקליט, ותחזרי לפה עם הטקסט
        response_text = "read=t=אנא שאל את שאלתך לאחר הצליל ולחץ סולמית&בדיקה=api_text_convert=yes&"
        return Response(response_text, mimetype='text/plain; charset=utf-8')
    
    # אם המשתמש כבר דיבר ויש טקסט - נחזיר לו את מה שהוא אמר
    return Response(f"read=t=הצלחה! אמרת: {user_text}&", mimetype='text/plain; charset=utf-8')

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice_endpoint():
    return handle_voice_logic()

@app.route('/', methods=['GET', 'POST'])
def home_endpoint():
    return handle_voice_logic()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
