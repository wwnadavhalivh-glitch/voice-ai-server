import os
from flask import Flask, request

app = Flask(__name__)

# נתיב ראשי (דף הבית) - כדי למנוע שגיאות 404 בבדיקות של Render
@app.route('/', methods=['GET'])
def home():
    return "השרת באוויר ופועל תקין!", 200

# הנתיב שאליו פונה ימות המשיח
@app.route('/webhook', methods=['POST', 'GET'])
def handle_voice():
    print("קריאה נכנסה מימות המשיח:", request.args)
    return "id_list_message=t-השרת של רנדר חובר בהצלחה למערכת הטלפונית."

if __name__ == '__main__':
    # קריאת הפורט ש-Render מגדיר במערכת (לרוב 10000), ואם לא נמצא אז ברירת מחדל 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
