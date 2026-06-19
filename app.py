from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_voice():
    # פקודת הדפסה שתמיד תופיע בלוגים אם פנו אלינו
    print("קיבלתי קריאה מ-POST!") 
    
    # בדיקה האם יש קבצים
    if request.files:
        print(f"התקבלו קבצים: {list(request.files.keys())}")
    
    # מחזירים "ok" מיידי כדי לא לנתק את השיחה
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
