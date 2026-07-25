import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "OK"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("--- קובץ שמע התקבל בשרת ---")
    
    if 'UploadFile' in request.files:
        audio_file = request.files['UploadFile']
        audio_file.save("user_recording.wav")
        print("הקובץ נשמר בהצלחה!")
        
        # השמעת הודעת תודה מובנית וניתוק
        return Response("play_and_get_audio=M1211&hangup=yes", mimetype='text/plain')

    return Response("hangup=yes", mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
