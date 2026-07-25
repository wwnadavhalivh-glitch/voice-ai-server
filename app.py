import os
from flask import Flask, request
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        print("Error: No file part in the request")
        return "No file", 400
    
    file = request.files['file']
    if file.filename == '':
        print("Error: No selected file")
        return "No file", 400

    # שמירת הקובץ הזמני (ימות המשיח שולחים בדרך כלל WAV או MP3)
    file_path = "temp_audio.wav"
    file.save(file_path)

    try:
        # המרה לפורמט WAV אם צריך ותמלול
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            # תמלול בעברית
            text = recognizer.recognize_google(audio_data, language='he-IL')
            
            print("\n" + "="*30)
            print(f"הודעה חדשה תומללה:")
            print(f"טקסט: {text}")
            print("="*30 + "\n")
            
    except sr.UnknownValueError:
        print("Log: Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Log: Could not request results; {e}")
    except Exception as e:
        print(f"Log: Error during transcription: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
