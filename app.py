from flask import Flask, request
import google.generativeai as genai
import os

app = Flask(__name__)

# הגדרת מפתח ה-API של גוגל ג'מיני
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # קבלת הטקסט המתומלל שהגיע מימות המשיח
    user_text = request.args.get('val_name') or request.args.get('Transcription') or request.args.get('search')
    
    # אם זו כניסה ראשונה או שעדיין לא נקלט טקסט
    if not user_text:
        # פקודה לימות המשיח להקליט את המשתמש ולתמלל
        return "read=t-מה תרצה לשאול? השמע את שאלתך בסיום הקש סולמית&api_audio_record=yes"

    try:
        # שליחת השאלה לג'מיני
        response = model.generate_content(user_text)
        answer = response.text
        
        # ניקוי תווים מיוחדים שעשויים להפריע להקראה הטלפונית
        clean_answer = answer.replace('*', '').replace('#', '').replace('\n', ' ')
        
        # החזרת התשובה להקראה + בקשה לשאלה נוספת
        return f"id_list_message=t-{clean_answer}&read=t-האם יש לך שאלה נוספת?&api_audio_record=yes"

    except Exception as e:
        print(f"Error: {e}")
        return "id_list_message=t-תרחשה שגיאה בעיבוד הבקשה, אנא נסה שוב מאוחר יותר."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
