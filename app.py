import os
from flask import Flask, request
from google import genai
from google.genai import types

app = Flask(__name__)

# אתחול ה-API של Gemini באמצעות המפתח שיוגדר ב-Render
# ה-SDK החדש מזהה אוטומטית את המשתנה GEMINI_API_KEY מהסביבה
client = genai.Client()

# משתנה גלובלי זמני לשמירת התשובה האחרונה עבור שלוחה 2
last_response_text = "עדיין לא התקבלה תשובה מהבינה המלאכותית."

# --- א. שלוחה 1 שולחת את קובץ ההקלטה לכאן ---
@app.route('/webhook', methods=['POST'])
def webhook():
    global last_response_text
    
    # בדיקה האם הגיע קובץ מימות המשיח (הם שולחים תחת השם 'file')
    if 'file' not in request.files:
        return "read=t-שגיאה. לא התקבל קובץ שמע.&hangup"
    
    audio_file = request.files['file']
    
    if audio_file.filename == '':
        return "read=t-שגיאה. קובץ ריק.&hangup"
    
    try:
        print("התקבלה הקלטה חדשה, מעבד עם Gemini...")
        
        # קריאת תוכן קובץ השמע ישירות לזיכרון
        audio_data = audio_file.read()
        
        # שליחת קובץ השמע ישירות למודל Gemini 2.5 Flash התומך באודיו
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=audio_data,
                    mime_type='audio/wav'  # ימות המשיח שולחים בפורמט WAV
                ),
                "האזן להקלטה זו, וענה על השאלה בקצר ובמילים פשוטות בעברית, ללא סימנים מיוחדים או כוכביות."
            ]
        )
        
        # שמירת התשובה שחזרה מהבינה המלאכותית
        last_response_text = response.text if response.text else "לא התקבלה תשובה תקינה."
        print(f"תשובת Gemini המוכנה: {last_response_text}")
        
        # פקודה לימות המשיח: להשמיע הודעה קצרה ולהעביר אוטומטית לשלוחה 2
        return "read=t-השאלה התקבלה ומעובדת. מעביר אותך לשמיעת התשובה.&go_to_folder=2"
        
    except Exception as e:
        print(f"שגיאה בעיבוד הנתונים: {e}")
        return "read=t-תקלה זמנית בחיבור לבינה המלאכותית.&hangup"

# --- ב. שלוחה 2 מושכת מכאן את התשובה (לטקסט לדיבור) ---
@app.route('/get-answer', methods=['GET', 'POST'])
def get_answer():
    global last_response_text
    # מחזיר את התשובה בפורמט שימות המשיח יודע להקריא (TTS)
    return f"read=t-{last_response_text}"

if __name__ == '__main__':
    # הרצה מקומית או דרך השרת
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
