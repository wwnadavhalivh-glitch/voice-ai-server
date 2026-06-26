import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/gemini-voice', methods=['GET', 'POST'])
def gemini_voice_endpoint():
    # ימות המשיח ישלחו את הקישור בקובץ הבא בפנייה השנייה
    audio_url = request.values.get('recording_file_link') or ''

    # שלב 1: פנייה ראשונית - השרת מורה לטלפון להקריא טקסט, להשמיע צליל ולהקליט
    if not audio_url:
        print("\n=== שיחה נכנסה: שולח פקודת הקלטה לטלפון ===")
        
        # מבנה הפקודה: read=t=הטקסט=שם_משתנה,מקש_סיום,מינימום_שניות,מקסימום_שניות,השמעה_לאישור,סוג_הקלטה,שמירה_בשלוחה
        # השתמשנו בסוג v (הקלטת קול) ובמשתנה recording_file_link
        instruction = "read=t=שלום כאן הבוט החכם שלך אנא הקלט את הודעתך לאחר הצליל=recording_file_link,hash,2,30,no,v,no&"
        return Response(instruction, mimetype='text/plain; charset=utf-8')

    # שלב 2: הטלפון סיים להקליט וחזר לשרת עם הקובץ
    print(f"\n=== הצלחה! הקובץ הוקלט ונשלח לשרת. הקישור: {audio_url} ===")
    
    return Response("read=t=ההקלטה שלך התקבלה בשרת בהצלחה, תודה=no,no,no&", mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
