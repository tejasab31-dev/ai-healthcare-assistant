import streamlit as st
import requests
from pdf_generator import generate_pdf
from history import get_prediction_history

st.set_page_config(
    page_title="AI Healthcare Assistant",
    page_icon="🩺",
    layout="centered"
)
with st.sidebar:
    st.title("🏥 AI Healthcare Assistant")
    st.write("Machine Learning Disease Prediction System")
    

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if st.session_state.user_name == "":

    st.title("🏥 Welcome to AI Healthcare Assistant")

    name = st.text_input("Enter Your Name")

    if st.button("Start"):
        if name.strip():
            st.session_state.user_name = name
            st.rerun()

    st.stop()
st.title(
    f"🩺 Welcome, {st.session_state.user_name}"
)

st.write(
    "Enter patient symptoms for disease prediction"
)

st.subheader("Select Symptoms")

itching = st.selectbox("Itching", [0,1])
skin_rash = st.selectbox("Skin Rash", [0,1])
joint_pain = st.selectbox("Joint Pain", [0,1])
stomach_pain = st.selectbox("Stomach Pain", [0,1])
vomiting = st.selectbox("Vomiting", [0,1])
fatigue = st.selectbox("Fatigue", [0,1])
headache = st.selectbox("Headache", [0,1])
nausea = st.selectbox("Nausea", [0,1])
cough = st.selectbox("Cough", [0,1])
high_fever = st.selectbox("High Fever", [0,1])

if st.button("🔍 Predict Disease"):

    data = {
        "itching": itching,
        "skin_rash": skin_rash,
        "joint_pain": joint_pain,
        "stomach_pain": stomach_pain,
        "vomiting": vomiting,
        "fatigue": fatigue,
        "headache": headache,
        "nausea": nausea,
        "cough": cough,
        "high_fever": high_fever
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=data
    )

    if response.status_code == 200:

     result = response.json()

    disease = result["prediction"]

    st.success(f"Predicted Disease: {disease}")

    st.info(f"Confidence Score: {result['confidence']}%")

    st.subheader("🤖 AI Health Advice")
    st.write(result["ai_advice"])
    pdf_file = generate_pdf(
    disease,
    result["confidence"],
    result["ai_advice"]
)
    with open(pdf_file, "rb") as pdf:

       st.download_button(
        label="📄 Download Health Report",
        data=pdf,
        file_name="health_report.pdf",
        mime="application/pdf"
    )

    
    if disease == "GERD":
            st.subheader("📋 Disease Description")
            st.write(
                "GERD (Gastroesophageal Reflux Disease) is a digestive disorder "
                "where stomach acid frequently flows back into the food pipe."
            )

            st.subheader("💡 Recommendations")
            st.write("✅ Avoid spicy foods")
            st.write("✅ Drink more water")
            st.write("✅ Avoid eating late at night")
            st.write("✅ Consult a doctor if symptoms continue")

    elif disease == "Allergy":
            st.subheader("📋 Disease Description")
            st.write(
                "An allergy occurs when the immune system reacts to substances "
                "such as pollen, dust, or certain foods."
            )

            st.subheader("💡 Recommendations")
            st.write("✅ Avoid allergens")
            st.write("✅ Keep surroundings clean")
            st.write("✅ Drink plenty of water")
            st.write("✅ Seek medical advice if severe")

    elif disease == "Fungal infection":
            st.subheader("📋 Disease Description")
            st.write(
                "Fungal infections are caused by fungi affecting skin, nails, "
                "or other body parts."
            )

            st.subheader("💡 Recommendations")
            st.write("✅ Maintain hygiene")
            st.write("✅ Keep skin dry")
            st.write("✅ Use prescribed medication")
            st.write("✅ Consult a dermatologist")
    elif disease == "AIDS":

            st.subheader("📋 Disease Description")
            st.write(
            "AIDS (Acquired Immunodeficiency Syndrome) is a chronic condition "
            "caused by HIV that weakens the immune system."
        )

            st.subheader("💡 Recommendations")
            st.write("✅ Consult a healthcare professional immediately")
            st.write("✅ Follow prescribed treatment")
            st.write("✅ Maintain a healthy lifestyle")
            st.write("✅ Avoid infections and risky exposures")
            st.write("✅ Attend regular medical checkups")

    else:
            st.subheader("💡 General Recommendation")
            st.write(
                "Please consult a healthcare professional for accurate diagnosis and treatment."
            ) 
    st.markdown("---")

st.subheader("📜 Prediction History")

if st.button("View History"):

    history_df = get_prediction_history()

    if len(history_df) > 0:
        st.dataframe(
            history_df,
            use_container_width=True
        )
    else:
        st.warning("No prediction history found.")