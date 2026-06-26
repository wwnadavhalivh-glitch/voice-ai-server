import os
from flask import Flask, request, Response

app = Flask(__name__)

# פונקציה ראשית שמטפלת בנתיב המבוקש מימות המשיח
@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice():
    # קריאת הפרמטר של הטקסט שימות המשיח שלחו
    user_text = request.args.get('ApiText', '').strip()
    
    print("=========================================")
    print(f"הטקסט שהתקבל מהטלפון: {user_text}")
    print("=========================================")

    if not user_text:
        return Response("read=t=הגעת לשרת בהצלחה. לא נקלט טקסט, אנא נסה שוב לאחר הצליל.&", mimetype='text/plain; charset=utf-8')
    
    response_text = f"read=t=הצלחה! השרת קלט שאמרת: {user_text}&"
    return Response(response_text, mimetype='text/plain; charset=utf-8')

# פונקציית גיבוי לנתיב הראשי של השרת במקרה הצורך
@app.route('/', methods=['GET', 'POST'])
def home():
    user_text = request.args.get('ApiText', '').strip()
    if user_text:
        return Response(f"read=t=הצלחה מהנתיב הראשי! אמרת: {user_text}&", mimetype='text/plain; charset=utf-8')
    return Response("read=t=השרת באוויר וממתין לפניות.&", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
