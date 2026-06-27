import os
from flask import Flask, request

app = Flask(__name__)

# דף הבית - כדי שנוכל לבדוק בדפדפן שהשרת חי
@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK - השרת באוויר ועובד!"

# נתיב קבלת הקובץ מימות המשיח
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    print("=== פנייה חדשה הגיעה לשרת! ===")
    
    # בדיקה האם ימות המשיח שלחו קובץ
    if 'file' in request.files:
        uploaded_file = request.files['file']
        print(f"קובץ התקבל בהצלחה! שם: {uploaded_file.filename}")
        
        # שמירה זמנית בשרת
        uploaded_file.save("test_file.wav")
        return "read=t-הקובץ הקיים נשלח ונקלט בשרת בהצלחה.&hangup"
        
    print("פנייה התקבלה, אך לא נמצא קובץ בשדה file")
    return "read=t-הגעת לשרת, אך לא נשלח קובץ.&hangup"

if __name__ == '__main__':
    # הרצה מקומית במידת הצורך
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
