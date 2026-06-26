import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice(*args, **kwargs):
    # שליפת הטקסט שהגיע מימות המשיח
    user_text = request.args.get('ApiText', '').strip()
    
    # הדפסה בולטת במיוחד ללוג של רנדר
    print("\n" + "="*40)
    print(f"!!! הטקסט שהתקבל מהטלפון: {user_text} !!!")
    print("="*40 + "\n")

    if not user_text:
        return Response("read=t=הגעת לשרת, אך הטקסט שהתקבל ריק. נסה לדבר שוב.&", mimetype='text/plain; charset=utf-8')
    
    # החזרת תשובה קולית שתשמע בטלפון
    return Response(f"read=t=השרת קלט בהצלחה את המילה: {user_text}&", mimetype='text/plain; charset=utf-8')

@app.route('/', methods=['GET', 'POST'])
def home(*args, **kwargs):
    return Response("read=t=השרת באוויר וממתין לפניות משלוחת ה-API.&", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
