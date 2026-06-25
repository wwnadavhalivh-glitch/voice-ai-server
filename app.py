from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def handle_voice():
    # הדפסת הנתונים שימות המשיח שולחת (בשביל הלוגים ב-Render)
    print("קריאה נכנסה מימות המשיח:", request.args)
    
    # החזרת פקודת טקסט לדיבור (TTS) שאומרת שהחיבור הצליח
    return "id_list_message=t-השרת של רנדר חובר בהצלחה למערכת הטלפונית."

if __name__ == '__main__':
    # השרת יאזין על פורט 5000 (מתאים להגדרות ברירת המחדל של Render)
    app.run(host='0.0.0.0', port=5000)
