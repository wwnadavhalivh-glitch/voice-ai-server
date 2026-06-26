import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice_endpoint():
    # מדפיס ללוג של רנדר שקיבלנו פנייה
    print("קיבלתי פנייה מימות המשיח!")
    
    # מחזיר הודעה פשוטה להשמעה בטלפון
    return Response("read=t=השרת מחובר בהצלחה=no,no,no&", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
