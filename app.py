import os
import requests
from flask import Flask, request

app = Flask(__name__)

# הגדרות ה-API הרשמיות של ימות המשיח
YM_BASE_URL = "https://www.call2all.co.il/ym/api"
YM_NUMBER = "0772228565"  # מספר המערכת שלך
YM_PASSWORD = "YOUR_YM_PASSWORD"  # <<< ודא ששמת כאן את הסיסמה האמיתית שלך!

@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK - השרת באוויר וממתין לפניות"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- פנייה חדשה התקבלה משלוחה 2 ---")
    
    token = f"{YM_NUMBER}:{YM_PASSWORD}"
    folder_path = "ym:2" # תיקייה 2 שבה נשמרות ההקלטות
    
    try:
        # שלב א': בקשת רשימת הקבצים בתיקייה כדי למצוא את הקובץ האחרון
        print(f"מבקש את רשימת הקבצים מתיקייה {folder_path}...")
        list_url = f"{YM_BASE_URL}/GetFileList"
        list_params = {
            'token': token,
            'path': folder_path
        }
        
        list_response = requests.get(list_url, params=list_params).json()
        
        # בדיקה האם התיקייה קיימת ויש בה קבצים
        if list_response.get('responseStatus') != 'OK' or 'files' not in list_response or not list_response['files']:
            print("לא נמצאו קבצים בתיקייה או שיש שגיאה בקבלת הרשימה.")
            return "read=t-התיקייה ריקה מקבצים.&hangup"
            
        # מיון הקבצים לפי תאריך העדכון האחרון שלהם כדי למצוא את הכי חדש
        all_files = list_response['files']
        # מסננים רק קבצים שמתחילים ב-tts ומסתיימים במספרים (או כל קובץ שמע)
        audio_files = [f for f in all_files if f.get('name', '').startswith('tts')]
        
        if not audio_files:
            audio_files = all_files # אם אין tts, ניקח את מה שיש
            
        # מציאת הקובץ האחרון שנוצר/עודכן
        latest_file_data = max(audio_files, key=lambda x: x.get('mtime', 0))
        latest_file_name = latest_file_data.get('name')
        
        print(f"הקובץ האחרון שזוהה בתיקייה הוא: {latest_file_name}")
        
        # שלב ב': הורדת הקובץ האחרון שזה עתה מצאנו
        download_url = f"{YM_BASE_URL}/DownloadFile"
        download_params = {
            'token': token,
            'path': f"{folder_path}/{latest_file_name}"
        }
        
        print(f"מתחיל למשוך את הקובץ {latest_file_name}...")
        download_response = requests.get(download_url, params=download_params, stream=True)
        
        if download_response.status_code == 200:
            # שמירת קובץ השמע המוקלט בשרת
            audio_path = "downloaded_audio.wav"
            with open(audio_path, 'wb') as f:
                for chunk in download_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            
            print(f"הקובץ {latest_file_name} נמשך בהצלחה ונשמר בשרת!")
            return "read=t-הקובץ האחרון זוהה ונמשך בהצלחה לשרת.&hangup"
        else:
            print(f"שגיאה בהורדת הקובץ. קוד סטטוס: {download_response.status_code}")
            return "read=t-תקלה בהורדת קובץ השמע.&hangup"
            
    except Exception as e:
        print(f"שגיאה בתהליך המשיכה החכם: {e}")
        return "read=t-שגיאה כללית בעיבוד הנתונים.&hangup"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
