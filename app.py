from flask import Flask, request
import google.generativeai as genai
import os

app = Flask(__name__)

# מפתח ה-API של גוגל ג'מיני
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # קבלת הטקסט המתומלל שנשלח מימות המשיח
    user_text = request.args.get('Transcription') or request.args.get('val_name') or request.args.get('search')
    
    # אם אין טקסט (כניסה ראשונית לשלוחה 1), נבקש הקלטה
    if not user_text:
        return "read=t-אנא השמע את שאלתך בצורה ברורה ובסיום הקש סולמית&api_audio_record=yes"

    try:
        # שליחת השאלה לג'מיני
        response = model.generate_content(user_text)
        answer = response.text
        
        # ניקוי תווים מיוחדים שעלולים להפריע להקראה הטלפונית
        clean_answer = answer.replace('*', '').replace('#', '').replace('\n', ' ').replace('&', ' ')
        
        # החזרת התשובה להקראה בשלוחה 2
        return f"id_list_message=t-{clean_answer}"

    except Exception as e:
        print(f"Error: {e}")
        return "id_list_message=t-תרחשה שגיאה בעיבוד הבקשה, אנא נסה שוב מאוחר יותר."

@app.route('/')
def home():
    return "השרת פעיל ומחובר בהצלחה"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
