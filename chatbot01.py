import streamlit as st
import pandas as pd
import google.generativeai as genai  # pip install google-generativeai
import os
from dotenv import load_dotenv
from datetime import datetime

# --- Step 1: Create & Store Build Info ---
build_info_file = "build_info.txt"

def create_build_info():
    """Creates a build info file with details."""
    build_info = f"""Build Information
--------------------------
Creator: Nitesh Kumar
Build Version: 1.0.0
Created On: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
© 2025 Nitesh Kumar. All rights reserved.
"""
    with open(build_info_file, "w") as file:
        file.write(build_info)

# Ensure build info file exists
if not os.path.exists(build_info_file):
    create_build_info()

def get_build_info():
    """Reads build info from the file."""
    if os.path.exists(build_info_file):
        with open(build_info_file, "r") as file:
            return file.read()
    return "Build info not found."

# Load datasets
faq_file_path = "BankFAQs.csv"
df_faq = pd.read_csv(faq_file_path)
loans_file_path = "Indian_Bank_Loans.xlsx"
df_loans = pd.read_excel(loans_file_path, engine="openpyxl")

# Load environment variables
load_dotenv()

# Retrieve API key from .env file
api_key = os.getenv("API_KEY")

# Initialize Gemini API
genai.configure(api_key=api_key)

# Function to find FAQ response
def find_faq_response(user_query):
    user_query_lower = user_query.lower()
    for _, row in df_faq.iterrows():
        if row["Question"].lower() in user_query_lower:
            return row["Answer"]
    return None

# Function to find loan details
def find_loan_info(bank, loan_type):
    relevant_loans = df_loans[(df_loans["Bank"] == bank) & (df_loans["Loan Type"] == loan_type)]
    if not relevant_loans.empty:
        row = relevant_loans.iloc[0]
        return f"\U0001F3E6 **{row['Bank']} - {row['Loan Type']}**\n\n\U0001F4C8 **Interest Rate:** {row['Interest Rate (per annum)']}%\n\U0001F4B0 **Loan Amount:** {row['Loan Amount']}\n\U0001F4C5 **Tenure:** {row['Tenure']} months"
    return "No relevant loan information found."

# EMI Calculation Function
def calculate_emi(principal, rate, tenure):
    try:
        if principal <= 0 or rate < 0 or tenure <= 0:
            return "Invalid input values. Please enter valid loan details."

        monthly_rate = rate / (12 * 100)  # Convert annual rate to monthly decimal
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
        
        total_payment = round(emi * tenure, 2)
        total_interest = round(total_payment - principal, 2)

        return {"emi": round(emi, 2), "total_payment": total_payment, "total_interest": total_interest}
    except Exception as e:
        return f"Error in calculation: {e}"

# Function to get AI response
def get_response(prompt):
    if "owner" in prompt.lower() or "who built you" in prompt.lower():
        return get_build_info()
    
    faq_response = find_faq_response(prompt)
    if faq_response:
        return faq_response

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Correct model initialization
        response = model.generate_content(prompt)  # Get AI response
        return response.text.strip() if hasattr(response, "text") else "No response from AI."
    except Exception as e:
        return f"Error retrieving response: {e}"

# Streamlit UI - Main Title
st.title("\U0001F4B0 Webcredit Chatbot")
st.write("Ask about **bank loans, interest rates, and FAQs**.")

# Sidebar EMI Calculator
st.sidebar.subheader("\U0001F4CA EMI Calculator")

principal = st.sidebar.number_input("\U0001F4B0 Loan Amount", min_value=1000, value=50000, step=1000)
rate = st.sidebar.number_input("\U0001F4C8 Interest Rate (per annum)", min_value=0.0, value=7.5, step=0.1)
tenure = st.sidebar.number_input("\U0001F4C5 Loan Tenure (in months)", min_value=1, value=60, step=1)

if st.sidebar.button("Calculate EMI"):
    result = calculate_emi(principal, rate, tenure)

    if isinstance(result, str):  # If error message is returned
        st.sidebar.error(result)
    else:
        st.sidebar.success(f"✅ **Monthly EMI:** ₹{result['emi']}")
        st.sidebar.write(f"💰 **Total Payment (Principal + Interest):** ₹{result['total_payment']}")
        st.sidebar.write(f"📊 **Total Interest Paid:** ₹{result['total_interest']}")

# Bank and Loan Type Selection
selected_bank = st.selectbox("🏦 Select Bank", df_loans["Bank"].unique())
selected_loan_type = st.selectbox("📄 Select Loan Type", df_loans[df_loans["Bank"] == selected_bank]["Loan Type"].unique())

if st.button("🔍 Get Loan Info"):
    loan_info = find_loan_info(selected_bank, selected_loan_type)
    st.write(loan_info)

# Chatbot Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display Chat History
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["message"])

# Chat Input
user_input = st.chat_input("💬 Ask me about loans, interest rates, and banking FAQs...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    response = get_response(user_input)
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    st.session_state.chat_history.append({"role": "assistant", "message": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)

    # Feedback Option
    feedback = st.radio("Was this response helpful?", ("Yes", "No"), index=None)
    if feedback == "No":
        improvement = st.text_input("How can we improve?")

