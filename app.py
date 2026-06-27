const express = require('express');
const multer = require('multer');
const { GoogleGenAI } = require('@google/genai');
const fs = require('fs');
const path = require('path');

const app = express();
const upload = multer({ dest: 'uploads/' });

// אתחול ה-API של Gemini עם המפתח שלך מתוך משתני הסביבה ב-Render
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

// משתנה גלובלי זמני לשמירת התשובה האחרונה (עבור שלוחה 2)
let lastResponseText = "עדיין לא התקבלה תשובה מהבינה המלאכותית.";

// --- א. שלוחה 1 שולחת את ההקלטה לכאן ---
app.post('/webhook', upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.send('read=t-שגיאה. לא התקבל קובץ שמע.&hangup');
        }

        console.log("התקבלה הקלטה חדשה, מעבד עם Gemini...");

        // 1. קריאת קובץ השמע שהגיע מימות המשיח
        const audioBuffer = fs.readFileSync(req.file.path);
        
        // 2. שליחת קובץ השמע ישירות ל-Gemini (מודל 2.5 Pro או Flash תומכים באודיו ישירות!)
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: [
                {
                    inlineData: {
                        mimeType: 'audio/wav', // ימות המשיח שולחים בפורמט WAV או AMR
                        data: audioBuffer.toString('base64')
                    }
                },
                { text: "האזן להקלטה זו, וענה על השאלה בקצר ובמילים פשוטות בעברית, ללא סימנים מיוחדים או כוכביות." }
            ]
        });

        // 3. שמירת התשובה שחזרה מה-AI
        lastResponseText = response.text || "לא התקבלה תשובה תקינה.";
        console.log("תשובת Gemini המוכנה:", lastResponseText);

        // 4. מחיקת הקובץ הזמני מהשרת
        fs.unlinkSync(req.file.path);

        // 5. החזרת תשובה למחייג: מעבירים אותו אוטומטית לשלוחה 2 לשמיעת התשובה
        // הפקודה go_to_folder=2 תעביר אותו ישירות לשלוחה 2
        res.send('read=t-השאלה התקבלה ומעובדת. מעביר אותך לשמיעת התשובה.&go_to_folder=2');

    } catch (error) {
        console.error("שגיאה בעיבוד:", error);
        res.send('read=t-תקלה זמנית בחיבור לבינה המלאכותית.&hangup');
    }
});

// --- ב. שלוחה 2 מושכת מכאן את התשובה (TTS - טקסט לדיבור) ---
app.get('/get-answer', (req, res) => {
    // ימות המשיח בשלוחת TTS קוראים קובץ הגדרות שמקריא טקסט דינמי
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.send(`read=t-${lastResponseText}`);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
