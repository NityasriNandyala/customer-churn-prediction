import streamlit as st
import requests
import os
import hashlib
from datetime import datetime

import pandas as pd

st.set_page_config(page_title="Churn Predictor", page_icon="📊", layout="centered")


def get_api_url():
    try:
        configured_url = st.secrets.get("CHURN_API_URL")
    except Exception:
        configured_url = None

    return configured_url or os.getenv(
        "CHURN_API_URL",
        "https://customer-churn-api.onrender.com/predict",
    )


API_URL = get_api_url()

st.markdown("""
<style>
:root {
    --ink: #17324d;
    --muted: #5d7285;
    --surface: #ffffff;
    --canvas: #f4f8fb;
    --teal: #087f8c;
    --teal-dark: #075e69;
    --gold: #f4b400;
}
.stApp {
    background: var(--canvas);
    color: var(--ink);
}
.block-container {
    max-width: 900px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
.stMarkdown, .stText, label, p {
    font-size: 1.08rem;
}
h1, h2, h3 {
    color: var(--ink);
    letter-spacing: 0;
}
h1 {
    font-size: 2.6rem !important;
    line-height: 1.1 !important;
}
h2 {
    margin-top: 1.4rem !important;
}
label {
    font-weight: 600;
}
input, select, textarea {
    font-size: 1.05rem !important;
}
button {
    min-height: 3rem;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
}
div[data-testid="stForm"], div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border: 1px solid #d9e5ec;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(23, 50, 77, 0.07);
    padding: 1.2rem;
}
div[data-testid="stFormSubmitButton"] button,
div[data-testid="stDownloadButton"] button {
    background: var(--teal);
    border-color: var(--teal);
    color: white;
}
div[data-testid="stFormSubmitButton"] button:hover,
div[data-testid="stDownloadButton"] button:hover {
    background: var(--teal-dark);
    border-color: var(--teal-dark);
    color: white;
}
div[data-testid="stMetric"] {
    background: var(--surface);
    border-left: 4px solid var(--teal);
    border-radius: 10px;
    padding: 0.8rem;
}
.hero {
    background: linear-gradient(120deg, #17324d 0%, #087f8c 100%);
    border-radius: 20px;
    color: white;
    margin: 0 0 1.5rem;
    padding: 2rem 2.2rem;
}
.hero-kicker {
    color: #b9edf0;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.hero h1 {
    color: white;
    margin: 0.4rem 0 0.7rem;
}
.hero p {
    color: #e5f6f7;
    margin: 0;
}
button:focus, input:focus, select:focus {
    outline: 3px solid #f4b400 !important;
    outline-offset: 2px;
}
</style>
""", unsafe_allow_html=True)

if "users" not in st.session_state:
    st.session_state.users = {}

if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


if st.session_state.authenticated_user is None:
    st.title("🔐 Account Access")
    st.caption("Sign in or create an account to use the customer churn predictor.")
    st.info("Use a username and a password with at least 6 characters.")

    sign_in, sign_up = st.tabs(["Sign in", "Sign up"])

    with sign_in:
        with st.form("sign_in_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            sign_in_submitted = st.form_submit_button("Sign in", use_container_width=True)

        if sign_in_submitted:
            stored_password = st.session_state.users.get(username.strip())
            if stored_password == hash_password(password):
                st.session_state.authenticated_user = username.strip()
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    with sign_up:
        with st.form("sign_up_form"):
            new_username = st.text_input("Choose a username")
            new_password = st.text_input("Choose a password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            sign_up_submitted = st.form_submit_button("Create account", use_container_width=True)

        if sign_up_submitted:
            username_key = new_username.strip()
            if len(username_key) < 3:
                st.error("Username must contain at least 3 characters.")
            elif len(new_password) < 6:
                st.error("Password must contain at least 6 characters.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif username_key in st.session_state.users:
                st.error("That username is already registered.")
            else:
                st.session_state.users[username_key] = hash_password(new_password)
                st.session_state.authenticated_user = username_key
                st.rerun()

    st.stop()

with st.sidebar:
    st.write(f"Signed in as **{st.session_state.authenticated_user}**")
    st.caption("Enter the customer details carefully. You can review the result before taking action.")
    st.divider()
    st.subheader("Session overview")
    st.metric("Assessments", len(st.session_state.prediction_history))
    high_risk_count = sum(
        item["Risk level"] == "High risk"
        for item in st.session_state.prediction_history
    )
    st.metric("High-risk cases", high_risk_count)
    if st.button("Sign out", use_container_width=True):
        st.session_state.authenticated_user = None
        st.rerun()

st.markdown(
    """
    <section class="hero">
        <div class="hero-kicker">Customer retention workspace</div>
        <h1>Customer Churn Intelligence</h1>
        <p>Turn account details into a clear next step for every customer.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    with st.form("customer_details"):
        st.subheader("🧾 Customer details")
        st.caption("Complete the customer profile below, then select Predict Churn Risk.")

        col1, col2, col3 = st.columns(3)

        with col1:
            gender = st.selectbox("Gender", ["Female", "Male"])
            senior_citizen = st.selectbox("Senior citizen", ["No", "Yes"])
            partner = st.selectbox("Partner", ["Yes", "No"])
            dependents = st.selectbox("Dependents", ["Yes", "No"])
            tenure = st.number_input(
                "Tenure (months)",
                0,
                72,
                help="How many months the customer has been with the company.",
            )
            phone_service = st.selectbox("Phone service", ["Yes", "No"])

        with col2:
            internet = st.selectbox("Internet service", ["DSL", "Fiber optic", "No"])
            online_security = st.selectbox("Online security", ["Yes", "No", "No internet service"])
            online_backup = st.selectbox("Online backup", ["Yes", "No", "No internet service"])
            device_protection = st.selectbox("Device protection", ["Yes", "No", "No internet service"])
            tech_support = st.selectbox("Tech support", ["Yes", "No", "No internet service"])
            streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])

        with col3:
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            paperless_billing = st.selectbox("Paperless billing", ["Yes", "No"])
            payment_method = st.selectbox(
                "Payment method",
                ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
            )
            monthly = st.number_input("Monthly charges", 0.0, 200.0)
            total = st.number_input("Total charges", 0.0, 10000.0)

        submitted = st.form_submit_button("🚀 Predict Churn Risk", use_container_width=True)

if submitted:
    if tenure > 0 and total < monthly:
        st.error("Total charges should be at least the current monthly charges for an existing customer.")
        st.stop()

    payload = {
        "gender": gender,
        "SeniorCitizen": 1 if senior_citizen == "Yes" else 0,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": int(tenure),
        "PhoneService": phone_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": float(monthly),
        "TotalCharges": float(total),
        "InternetService": internet
    }

    try:
        with st.spinner("Analyzing customer behavior..."):
            res = requests.post(API_URL, json=payload, timeout=15)

        if res.status_code == 200:
            data = res.json()
            prob = float(data["probability"])
            probability_percent = round(prob * 100)

            # ---------- Result ----------
            st.subheader("📊 Prediction Result")
            st.metric("Churn probability", f"{probability_percent}%")

            if prob > 0.7:
                risk_level = "High risk"
                st.error(f"🔴 High Risk of Churn ({prob})")
            elif prob > 0.4:
                risk_level = "Moderate risk"
                st.warning(f"🟡 Moderate Risk ({prob})")
            else:
                risk_level = "Low risk"
                st.success(f"🟢 Low Risk ({prob})")

            st.markdown(f"**Risk level:** {risk_level}. The estimated chance of churn is {probability_percent}%.")

            st.session_state.prediction_history.insert(0, {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Risk level": risk_level,
                "Probability": f"{probability_percent}%",
                "Months": int(tenure),
                "Monthly bill": f"${monthly:,.2f}",
                "Contract": contract,
                "Internet": internet,
                "Recommended action": data.get("recommended_action", "N/A"),
            })
            st.session_state.prediction_history = st.session_state.prediction_history[:10]

            # ---------- Progress Bar ----------
            st.progress(min(int(prob * 100), 100))

            # ---------- Insights ----------
            st.subheader("🧠 Insights")

            if data.get("reasons"):
                for r in data["reasons"]:
                    st.write(f"• {r}")
            else:
                st.info("✅ Customer is stable. No major risk factors detected.")

            # ---------- Recommendation ----------
            st.subheader("💡 Recommended Action")
            st.info(data.get("recommended_action", "N/A"))

        else:
            st.error(f"API Error: {res.status_code}")
            st.write(res.text)

    except Exception as e:
        st.warning("⏳ Server might be waking up, try again...")
        st.error(str(e))

if st.session_state.prediction_history:
    st.divider()
    st.subheader("🗂️ Recent assessments")
    st.caption("Your last 10 assessments are kept in this browser session.")
    history_df = pd.DataFrame(st.session_state.prediction_history)
    st.dataframe(history_df, hide_index=True, use_container_width=True)
    st.download_button(
        "Download assessment history",
        history_df.to_csv(index=False).encode("utf-8"),
        "churn-assessment-history.csv",
        "text/csv",
        use_container_width=True,
    )