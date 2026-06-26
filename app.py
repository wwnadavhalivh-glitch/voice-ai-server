import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice_endpoint():
    # בדיקה האם כבר חזר אלינו קובץ שמע מימות המשיח
    audio_url = request.values.get('recording_file_link') or request.values.get('file_url') or ''

    # שלב א': אם זו פנייה ראשונית ואין קובץ - השרת שולח הוראות הקלטה לטלפון
    if not audio_url:
        print("\n=== שיחה נכנסה: שולח פקודות הקלטה לטלפון ===")
        
        # פקודות משורשרות (rapi): 
        # 000: השמעת הטקסט שלך
        # 001: השמעת צפצוף (beep)
        # 002: הקלטה לתיקייה זמנית, זיהוי 3 שניות שתיקה ושליחה חזרה לשרת (yes)
        instructions = (
            "api_000=rapi,,say_text,שלום כאן הבוט החכם שלך אנא הקלט את הודעתך לאחר הצליל&"
            "api_001=rapi,,play_sound,beep&"
            "api_002=rapi,,record,/gemini_temp/auto,,yes,3,1&"
        )
        return Response(instructions, mimetype='text/plain; charset=utf-8')

    # שלב ב': הטלפון סיים להקליט וחזר לשרת עם הקובץ!
    print(f"\n=== הצלחה! הקובץ הוקלט ונשלח לשרת. הקישור: {audio_url} ===")
    
    # כרגע רק נשמיע למשתמש שהקובץ התקבל בהצלחה כדי לראות שהכל עובד
    return Response("read=t=ההקלטה שלך התקבל בשרת בהצלחה, תודה=no,no,no&", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
