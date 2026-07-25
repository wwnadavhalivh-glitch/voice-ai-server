from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # קבלת פרמטרים שונים שבהם ימות המשיח עשויים לשלוח את הטקסט המתומלל
    user_text = (
        request.args.get('val_name') or 
        request.args.get('Transcription') or 
        request.args.get('search') or
        request.args.get('v_000')
    )
    
    print(f"DEBUG - Text received from Yemot: {user_text}")

    # אם זו כניסה ראשונה (עדיין לא התקבל טקסט)
    if not user_text or user_text.strip() == "":
        # פקודה לימות המשיח לבצע הקלטה ותמלול
        return "read=t-מה תרצה לשאול? השמע את שאלתך ובסיום הקש סולמית&api_audio_record=yes"

    # במידה והתקבל טקסט מתומלל בהצלחה
    return f"id_list_message=t-השאלה נקלטה בהצלחה. השאלה הייתה: {user_text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
