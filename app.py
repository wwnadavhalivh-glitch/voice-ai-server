import os
import requests
from flask import Flask, request

app = Flask(__name__)

# פרטי החיבור ל-API של ימות המשיח לצורך משיכת קבצים
# (הפרטים נלקחו מצילום המסך של המערכת שלך)
YM_API_URL = "https://ymest.co.il/api/DownloadFile"
YM_NUMBER = "0772228565"  # מספר המערכת שלך
YM_PASSWORD = "YOUR_YM_PASSWORD"  # <<< החלף כאן בסיסמה הסודית שלך לימות המשיח!

@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK - השרת באוויר וממתין לפניות"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- פנייה חדשה התקבלה משלוחה 2 ---")
    
    # הכתובת שממנה נמשוך את הקובץ בתיקייה 2 (לפי הגדרת ימות המשיח)
    # נבקש את הקובץ האחרון שהוקלט שם (למשל tts.000 או 000.wav)
    # הערה: אם הקבצים נשמרים בשמות מותאמים, ניתן למשוך לפי רשימת קבצים,
    # כרגע ננסה למשוך את קובץ ברירת המחדל הקיים בתיקייה 2:
    target_path = "ym:2/tts.000" 
    
    # בניית הבקשה להורדת הקובץ מימות המשיח לשרת שלנו
    params = {
        'token': f"{YM_NUMBER}:{YM_PASSWORD}",
        'path': target_path
    }
    
    try:
        print(f"מנסה למשוך את הקובץ {target_path} מימות המשיח...")
        ym_response = requests.get(YM_API_URL, params=params, stream=True)
        
        if ym_response.status_code == 200:
            # שמירת קובץ השמע המוקלט על השרת ברנדר
            audio_path = "downloaded_audio.wav"
            with open(audio_path, 'wb') as f:
                for chunk in ym_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            
            print("הקובץ נמשך בהצלחה ונשמר בשרת!")
            
            # כאן בהמשך נכניס את הקישור ל-Gemini.
            # כרגע נחזיר הודעה למשתמש שהקובץ נקלט וננתק (או נעביר לשלוחה 3 בהמשך)
            return "read=t-ההקלטה שלך נמשכה בהצלחה על ידי השרת.&hangup"
            
        else:
            print(f"שגיאה במשיכת הקובץ מימות המשיח. קוד שגיאה: {ym_response.status_code}")
            return "read=t-תקלה במשיכת קובץ השמע מהמערכת.&hangup"
            
    except Exception as e:
        print(f"שגיאה בתקשורת: {e}")
        return "read=t-שגיאה כללית בעיבוד הנתונים.&hangup"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
