from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_voice():
    # בדיקה האם הגיע קובץ קול
    if 'file' in request.files:
        audio_file = request.files['file']
        audio_file.save("received_audio.mp3")
        print("קובץ אודיו התקבל ונשמר!")
        return "קיבלתי את ההקלטה"
    else:
        return "לא התקבל קובץ"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
