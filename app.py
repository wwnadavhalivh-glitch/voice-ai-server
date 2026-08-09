import gc
import os
from flask import Flask, Response, request
from google import genai

app = Flask(__name__)
api_key = (
    os.environ.get("GEMINI_API_KEY")
    or os.environ.get("GEMINI_API_KEY_1")
    or os.environ.get("GEMINI_API_KEY_2")
)
client = genai.Client(api_key=api_key)

# מילון זמני לשמירת קריאות אחרונות למניעת כפילויות
recent_calls = {}


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
  print("--- קבלה פניה חדשה ממוקד הטלפוניה ---")
  args = request.args.to_dict()
  print(f"Args (GET): {args}")

  api_call_id = args.get("ApiCallId")

  # בדיקה אם הבקשה הזו כבר טופלה ממש עכשיו (מניעת כפילות משרת הטלפוניה)
  if api_call_id and api_call_id in recent_calls:
    print(f"--- בקשה כפולה זוהתה עבור ApiCallId: {api_call_id} ---")
    # מחזירים את התשובה שכבר ניתנה או ריק כדי לא ליצור כפילות שמע
    return Response(recent_calls[api_call_id], mimetype="text/plain; charset=utf-8")

  user_text = args.get("text")
  hangup_status = args.get("hangup")

  if user_text:
    print(f"--- הנתונים שהתקבלו מהמשתמש: {user_text} ===")

    # שליחת הטקסט לג'מיני
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=(
            "ענה בעברית פשוטה ובלי סמלים מיוחדים, וגם בלי נקודות, כוכביות או"
            f" פסיקים על השאלה הבאה: {user_text}"
        ),
    )
    ai_answer = response.text.strip().replace("\n", " ")
    print(f"--- התקבלה תשובה מג'מיני: {ai_answer} ===")

    response_text = f"id_list_message=t-{ai_answer}&hangup=yes"
    gc.collect()

    # שמירת התשובה במטמון עבור ה-ApiCallId הזה למקרה שתגיע כפילות
    if api_call_id:
      recent_calls[api_call_id] = response_text

    return Response(response_text, mimetype="text/plain; charset=utf-8")

  else:
    # ברירת מחדל: שליחת המקלדת והקלטת קול
    response_text = "read=t=אנא הקלט את הודעתך לאחר הצליל ובסיום הקש סולמית=text,,voice,no_say_recording=yes"
    gc.collect()
    return Response(response_text, mimetype="text/plain; charset=utf-8")


@app.route("/")
def home():
  return "Voice AI Server is running!"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=10000)
