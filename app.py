import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice():
    # ימות המשיח שולחים את נתיב קובץ השמע שהוקלט באחד מהפרמטרים הבאים:
    file_url = request.args.get('ApiFileUrl', '')
    file_name = request.args.get('ApiFileName', '')
    
    print("=========================================")
    print(" פנייה חדשה התקבלה מהטלפון!")
    print(f"קישור לקובץ השמע: {file_url}")
    print(f"שם הקובץ שהוקלט: {file_name}")
    print("=========================================")

    # תגובה חזרה לימות המשיח כדי שהשיחה לא תתנתק בשגיאה
    if file_url:
        return Response("read=t=קובץ השמע התקבל בשרת בהצלחה.&", mimetype='text/plain; charset=utf-8')
    else:
        return Response("read=t=הגעת לשרת, אך קובץ השמע לא נמצא בפנייה.&", mimetype='text/plain; charset=utf-8')

@app.route('/', methods=['GET', 'POST'])
def home():
    return Response("השרת באוויר וממתין לקבצי שמע.&", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
