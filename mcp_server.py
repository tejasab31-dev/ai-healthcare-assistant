from click import prompt
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
from openai import OpenAI
from config import OPENAI_API_KEY
import sqlite3


app = FastAPI()

model = pickle.load(open("model/disease_model.pkl", "rb"))
client = OpenAI(api_key=OPENAI_API_KEY)

class Symptoms(BaseModel):
    itching: int
    skin_rash: int
    joint_pain: int
    stomach_pain: int
    vomiting: int
    fatigue: int
    headache: int
    nausea: int
    cough: int
    high_fever: int

@app.get("/")
def home():
    return {"message": "Healthcare MCP Server Running Successfully"}

@app.post("/predict")
def predict(symptom: Symptoms):

    input_data = pd.DataFrame([{
        "itching": symptom.itching,
        "skin_rash": symptom.skin_rash,
        "joint_pain": symptom.joint_pain,
        "stomach_pain": symptom.stomach_pain,
        "vomiting": symptom.vomiting,
        "fatigue": symptom.fatigue,
        "headache": symptom.headache,
        "nausea": symptom.nausea,
        "cough": symptom.cough,
        "high_fever": symptom.high_fever
    }])

    prediction = model.predict(input_data)
    disease = str(prediction[0])

    prompt = f"""
                You are a healthcare assistant.

                    Predicted disease: {disease}

                    Provide:
                    1. Disease explanation
                    2. Common causes
                    3. Recommended diet
                    4. Precautions
                    5. When to consult a doctor

                    Keep it concise and easy to understand.
                        """

    ai_advice = "OpenAI test successful"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        ai_advice = response.choices[0].message.content
    except Exception as e:
        ai_advice = f"OpenAI Error: {str(e)}"
    probability = model.predict_proba(input_data)
    confidence = max(probability[0]) * 100
    

    conn = sqlite3.connect("healthcare.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (disease, confidence)
        VALUES (?, ?)
        """,
        (disease, round(confidence, 2))
    )

    conn.commit()
    conn.close()

    return {
        "prediction": disease,
        "confidence": round(confidence, 2),
        "ai_advice": ai_advice
    }