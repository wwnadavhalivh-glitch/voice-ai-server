from flask import Flask, request, Response
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/webhook', methods=['POST'])
def handle_voice():
    # קבלת הקלט מהטלפון (מה שהמשתמש אמר)
    user_text = request.values.get('data', 'שלום') 
    
    # פנייה מהירה ל-GPT
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_text}]
    )
    ai_text = completion.choices[0].message.content
    
    # כאן אנחנו חייבים לחזור מהר. 
    # לצורך הבדיקה נשתמש בטקסט שימות המשיח יקראו (TTS של ימות המשיח)
    # זה הכי מהיר שיש!
    return f"say=הנה התשובה שלי: {ai_text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
