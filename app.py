from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # קבלת הטקסט המתומלל במידה וימות המשיח כבר שלחו אותו
    user_text = (
        request.args.get('Transcription') or 
        request.args.get('val_name') or 
        request.args.get('search') or
        request.args.get('v_000')
    )
    
    print(f"DEBUG - Text received from Yemot: {user_text}")

    # אם זו פנייה ראשונה (עדיין לא התקבל טקסט)
    if not user_text or user_text.strip() == "":
        # t-1234 הוא קובץ ההודעה ("אנא הקלט את שאלתך ובסיום הקש סולמית")
        # הפרמטר tap מפעיל צליל (ביפ) לפני תחילת ההקלטה
        return "read=t-אנא הקלט את שאלתך ובסיום הקש סולמית=val_1,1,1,7,Y,No,N,tap&api_audio_record=yes"

    # ברגע שהתקבל הטקסט מההקלטה והתמלול
    print(f"SUCCESS: Received prompt: {user_text}")
    return f"id_list_message=t-הטקסט נקלט בהצלחה בשרת: {user_text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
