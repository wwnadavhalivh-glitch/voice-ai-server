import os
from flask import Flask, request, Response

app = Flask(__name__)

# פונקציית עזר משותפת שרק קוראת את הטקסט ומדפיסה
def handle_voice_logic():
    # קריאת הפרמטר מכל סוגי הבקשות (GET, POST, URL, FORM)
    user_text = request.values.get('ApiText', '').strip()
    
    print("\n" + "="*40)
    print(f"!!! הטקסט שהתקבל מהטלפון: {user_text} !!!")
    print("="*40 + "\n")

    if not user_text:
        return Response("read=t=הגעת לשרת בהצלחה. לא נקלט טקסט, אנא נסה שוב לאחר הצליל.&", mimetype='text/plain; charset=utf-8')
    
    return Response(f"read=t=הצלחה! השרת קלט שאמרת: {user_text}&", mimetype='text/plain; charset=utf-8')

# נתיב ראשון
@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice_endpoint():
    return handle_voice_logic()

# נתיב שני לגיבוי
@app.route('/', methods=['GET', 'POST'])
def home_endpoint():
    return handle_voice_logic()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
