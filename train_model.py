"""
train_model.py

Train a Water Quality classifier pipeline and save model.pkl.
If 'water.csv' exists in the project root it will be used.
Otherwise a small synthetic dataset will be generated so the app works immediately.
Usage:
    python train_model.py
Outputs:
    model.pkl (saved sklearn pipeline)
    sample_water.csv (if generated)
"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

root = Path(__file__).resolve().parent
csv_path = root / "water.csv"

if csv_path.exists():
    print("Found water.csv - using it for training.")
    df = pd.read_csv(csv_path)
else:
    # generate a tiny synthetic dataset and save as sample_water.csv
    print(" Generating a small synthetic dataset (sample_water.csv).")
    np.random.seed(42)
    n = 200
    df = pd.DataFrame({
        "ph": np.random.normal(7, 0.8, size=n),
        "Hardness": np.random.normal(150, 30, size=n),
        "Solids": np.random.normal(7000, 2000, size=n),
        "Chloramines": np.random.normal(3, 0.8, size=n),
        "Conductivity": np.random.normal(400, 100, size=n),
        "Organic_carbon": np.random.normal(10, 3, size=n),
        "Trihalomethanes": np.random.normal(70, 20, size=n),
        "Turbidity": np.random.normal(3, 1, size=n),
    })
    # simple rule for potability (for demo only)
    df["Potability"] = ((df["ph"].between(6.5,8.5)) & (df["Turbidity"] < 5) & (df["Chloramines"] < 5)).astype(int)
    df.to_csv(root/"sample_water.csv", index=False)
    print("Saved sample_water.csv")

# Basic cleaning: keep only numeric columns and required target
if "Potability" not in df.columns:
    raise ValueError("Dataset must contain 'Potability' column as target (0/1).")

X = df.drop("Potability", axis=1)
y = df["Potability"]

numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
X = X[numeric_cols]

pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier(n_estimators=150, random_state=42))
])

pipeline.fit(X, y)

out_path = root / "model.pkl"
joblib.dump(pipeline, out_path)
print("Trained pipeline saved to model.pkl")