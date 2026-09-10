# 🌊 Water Quality & Potability Prediction System

An end-to-end Machine Learning web application that analyzes key chemical water parameters and predicts whether water is **SAFE** or **NOT SAFE** for drinking. Includes confidence scoring, localized automated safety suggestions, and multilingual audio feedback (English, Hindi, Telugu).

---

## 🌟 Key Features
- **Machine Learning Classification**: Predicts water potability based on 8 chemical features (`pH`, `Hardness`, `Solids`, `Chloramines`, `Conductivity`, `Organic Carbon`, `Trihalomethanes`, `Turbidity`).
- **Confidence Rating**: Displays prediction probability & confidence metrics.
- **Multilingual Support**: Supports English, Hindi (हिंदी), and Telugu (తెలుగు) UI translations and automatic text-to-speech audio guidance.
- **Safety Suggestions**: Provides automatic actionable filtration and safety instructions when water is unsafe.
- **Production Ready**: Prepared for 24/7 cloud hosting on Render / Heroku / Railway.

---

## 📁 Repository Structure
```
water_quality_project/
├── app.py                 # Flask web application & translation logic
├── train_model.py         # Model training script
├── model.pkl              # Trained Machine Learning pipeline
├── requirements.txt       # Production Python dependencies
├── Procfile               # Web server configuration for Cloud Hosting
├── .gitignore             # Git ignore list
├── sample_water.csv       # Water quality dataset
├── static/                # CSS styles & dynamic audio files
└── templates/             # HTML UI templates (home.html, index.html)
```

---

## 🚀 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/water-quality-project.git
   cd water-quality-project
   ```

2. **Create and activate a Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   # source venv/bin/activate  # macOS / Linux
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your web browser.

---

## 🌐 Deploy to Cloud (Render)
1. Push this repository to **GitHub**.
2. Connect repository to [Render.com](https://render.com).
3. Set Start Command to: `gunicorn app:app`.
4. Click **Deploy**!
