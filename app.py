from flask import Flask, render_template, request
from gtts import gTTS
import os
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("model.pkl")

# -------------------------
# TRANSLATIONS
# -------------------------

translations = {

    "hi": {
        "SAFE for Drinking": "पीने के लिए सुरक्षित",
        "NOT SAFE for Drinking": "पीने के लिए सुरक्षित नहीं",
        "Result": "परिणाम",
        "Confidence": "विश्वास स्तर",
        "Automatic Safety Suggestions": "स्वचालित सुरक्षा सुझाव",

        "Improve filtration system.": "फिल्ट्रेशन सिस्टम में सुधार करें।",
        "Boil water before drinking.": "पीने से पहले पानी उबालें।",
        "Install RO system.": "आरओ सिस्टम लगाएं।",
        "Water quality is good. Maintain regular testing.": "पानी की गुणवत्ता अच्छी है। नियमित जांच बनाए रखें।"
    },

    "te": {
        "SAFE for Drinking": "తాగడానికి సురక్షితం",
        "NOT SAFE for Drinking": "తాగడానికి సురక్షితం కాదు",
        "Result": "ఫలితం",
        "Confidence": "నమ్మకం స్థాయి",
        "Automatic Safety Suggestions": "స్వయంచాలక భద్రత సూచనలు",

        "Improve filtration system.": "ఫిల్టరేషన్ వ్యవస్థను మెరుగుపరచండి.",
        "Boil water before drinking.": "తాగడానికి ముందు నీటిని మరిగించండి.",
        "Install RO system.": "ఆర్ఓ వ్యవస్థను ఏర్పాటు చేయండి.",
        "Water quality is good. Maintain regular testing.": "నీటి నాణ్యత మంచిది. నియమిత పరీక్షలు కొనసాగించండి."
    }
}

# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def home():
    return render_template("home.html")


# -------------------------
# FORM PAGE
# -------------------------

@app.route("/predict_page")
def predict_page():
    return render_template("index.html")


# -------------------------
# PREDICTION
# -------------------------

@app.route("/predict", methods=["POST"])
def predict():

    ph=float(request.form["ph"])
    hardness=float(request.form["hardness"])
    solids=float(request.form["solids"])
    chloramines=float(request.form["chloramines"])
    conductivity=float(request.form["conductivity"])
    organic_carbon=float(request.form["organic_carbon"])
    trihalomethanes=float(request.form["trihalomethanes"])
    turbidity=float(request.form["turbidity"])

    language=request.form["language"]

    data=np.array([[ph,hardness,solids,chloramines,
                    conductivity,organic_carbon,
                    trihalomethanes,turbidity]])

    prediction=model.predict(data)[0]
    probability=model.predict_proba(data)[0].max()

    prob=round(probability,2)

    if prediction==1:
        result="SAFE for Drinking"
        suggestions=["Water quality is good. Maintain regular testing."]
    else:
        result="NOT SAFE for Drinking"
        suggestions=[
            "Improve filtration system.",
            "Boil water before drinking.",
            "Install RO system."
        ]

    heading_result="Result"
    heading_confidence="Confidence"
    heading_suggestions="Automatic Safety Suggestions"

    if language in translations:

        result=translations[language].get(result,result)

        heading_result=translations[language].get("Result",heading_result)
        heading_confidence=translations[language].get("Confidence",heading_confidence)
        heading_suggestions=translations[language].get("Automatic Safety Suggestions",heading_suggestions)

        suggestions=[translations[language].get(s,s) for s in suggestions]

    speech_text=result+". "

    for s in suggestions:
        speech_text+=s+". "

    if language=="hi":
        lang_code="hi"
    elif language=="te":
        lang_code="te"
    else:
        lang_code="en"

    audio_filename=f"output_{language}.mp3"
    audio_path=os.path.join("static",audio_filename)

    try:

        if os.path.exists(audio_path):
            os.remove(audio_path)

        tts=gTTS(text=speech_text,lang=lang_code)
        tts.save(audio_path)

    except:
        audio_filename=None

    return render_template(
        "index.html",
        result=result,
        prob=prob,
        suggestions=suggestions,
        heading_result=heading_result,
        heading_confidence=heading_confidence,
        heading_suggestions=heading_suggestions,
        audio_file=audio_filename,

        prediction=prediction,

        ph=ph,
        hardness=hardness,
        solids=solids,
        chloramines=chloramines,
        conductivity=conductivity,
        organic_carbon=organic_carbon,
        trihalomethanes=trihalomethanes,
        turbidity=turbidity
    )


if __name__=="__main__":
    app.run(debug=True)