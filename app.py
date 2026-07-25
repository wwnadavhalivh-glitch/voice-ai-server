from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # חילוץ הטקסט המתומלל שמגיע מימות המשיח
    user_text = request.args.get('Transcription') or request.args.get('val_name') or request.args.get('search')
    
    # הדפסת הנתונים שיופיעו ביומן ההרצה ב-Render
    print("=" * 40)
    print(f"DEBUG - Text received from Yemot: {user_text}")
    print("=" * 40)
    
    if not user_text:
        # פנייה ראשונה: ימות המשיח מבקשים להקליט
        return "read=t-אנא השמע את שאלתך ובסיום הקש סולמית&api_audio_record=yes"
    
    # פנייה שנייה: הקלטה נקלטה ופוענחה בהצלחה
    return "id_list_message=t-ההודעה התקבלה בהצלחה בשרת"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
