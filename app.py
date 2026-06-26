import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice_endpoint():
    print(f"\n=== התקבלה פנייה! פרמטרים: {dict(request.values)} ===")
    
    # פקודה פשוטה להשמעת טקסט בלבד, ללא הקלטה
    return Response("read=t=שלום, השרת מחובר בהצלחה=no,no,no&", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
