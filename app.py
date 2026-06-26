import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/gemini-voice', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def gemini_voice(*args, **kwargs):  # הוספנו תמיכה בקבלת משתנים כדי למנוע את הקריסה
    # קריאת הפרמטר של הטקסט שימות המשיח שלחו
    user_text = request.args.get('ApiText', '').strip()
    
    print("=========================================")
    print(f"הטקסט שהתקבל מהטלפון: {user_text}")
    print("=========================================")

    if not user_text:
        # אם הגיע ריק, נבקש ממנו לדבר שוב
        return Response("read=t=הגעת לשרת בהצלחה. לא נקלט טקסט, אנא נסה שוב לאחר הצליל.&", mimetype='text/plain; charset=utf-8')
    
    # אם הטקסט הגיע - נחזיר אותו כדי לשמוע שהכל עובד
    response_text = f"read=t=הצלחה! השרת קלט שאמרת: {user_text}&"
    return Response(response_text, mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
