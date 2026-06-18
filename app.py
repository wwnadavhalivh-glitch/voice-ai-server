from flask import Flask, Response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_voice():
    # תגובה מיידית לימות המשיח
    print("קיבלתי קריאה, מגיב מייד!")
    return Response("<speak>שלום, המערכת עובדת בהצלחה</speak>", mimetype='application/xml')
