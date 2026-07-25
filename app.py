from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # קבלת הטקסט המתומלל מתוך הפרמטרים שאימו ימות המשיח
    user_text = request.args.get('val_name') or request.args.get('Transcription') or request.args.get('search')
    
    print(f"DEBUG - Text received from Yemot: {user_text}")

    # אם עדיין לא התקבל טקסט (כניסה ראשונית לשלוחה)
    if not user_text:
        # פקודה לימות המשיח לבקש מהמשתמש לדבר ולהקליט
        return "read=t-מה תרצה לשאול? השמע את שאלתך ובסיום הקש סולמית&api_audio_record=yes"

    # במידה והתקבל טקסט
    return f"id_list_message=t-השאלה שהתקבלה היא {user_text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
