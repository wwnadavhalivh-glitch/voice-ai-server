import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/gemini-voice', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def gemini_voice():
    # 1. קריאת הפרמטר של הטקסט שימות המשיח שלחו
    user_text = request.args.get('ApiText', '').strip()
    
    # 2. הדפסה ברורה ללוג של Render (זה מה שיופיע לך במסך)
    print("=========================================")
    print(f"הטקסט שהתקבל מהטלפון: {user_text}")
    print("=========================================")

    # 3. בדיקה אם הטקסט הגיע ריק
    if not user_text:
        response_text = "read=t=הגעת לשרת בהצלחה, אך לא נקלט שום טקסט. אנא נסה לדבר חזק יותר לאחר הצליל.&"
        return Response(response_text, mimetype='text/plain; charset=utf-8')
    
    # 4. אם הטקסט הגיע - נחזיר אותו למערכת כדי שהיא תקריא לך אותו בחזרה
    response_text = f"read=t=הטקסט התקבל בשרת בהצלחה! אתה אמרת: {user_text}&"
    return Response(response_text, mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
