from flask import Flask, request, Response
from openai import OpenAI
from gtts import gTTS
import os

app = Flask(__name__)
client = OpenAI(api_key="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")

@app.route('/voice-ai', methods=['POST'])
def handle_voice():
    # כאן יגיע האודיו מימות המשיח
    user_text = "שלום, איך אני יכול לעזור?" # בעתיד נחבר כאן STT
    
    # שליחה ל-OpenAI לקבלת תשובה
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_text}]
    )
    ai_text = response.choices[0].message.content
    
    # המרת טקסט לקול בעברית
    tts = gTTS(text=ai_text, lang='iw')
    tts.save("response.mp3")
    
    # החזרת הקובץ לטלפון
    return Response(open("response.mp3", "rb").read(), mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
