import streamlit as st
import pandas as pd
import google.generativeai as genai  # pip install google-generativeai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API key from .env file
api_key = os.getenv("API_KEY")

# Initialize Gemini API
genai.configure(api_key=api_key)

# Load datasets
faq_file_path = "BankFAQs.csv"
df_faq = pd.read_csv(faq_file_path)
loans_file_path = "Indian_Bank_Loans.xlsx"
df_loans = pd.read_excel(loans_file_path, engine="openpyxl")

def find_faq_response(user_query):
    user_query_lower = user_query.lower()
    for _, row in df_faq.iterrows():
        if row["Question"].lower() in user_query_lower:
            return row["Answer"]
    return None

def find_loan_info(user_query):
    user_query_lower = user_query.lower()
    for _, row in df_loans.iterrows():
        if row["Bank"].lower() in user_query_lower or row["Loan Type"].lower() in user_query_lower:
            return f"{row['Bank']} - {row['Loan Type']}: {row['Interest Rate (per annum)']}, {row['Loan Amount']}, {row['Tenure']}"
    return None

def get_response(prompt):
    """Get response from FAQ, Indian Bank Loans dataset, or fallback to Gemini AI."""
    faq_response = find_faq_response(prompt)
    if faq_response:
        return faq_response
    
    loan_response = find_loan_info(prompt)
    if loan_response:
        return loan_response

    # If no match found, use Gemini API
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    st.title("Google GenAI-powered Fintech Chatbot")
    st.write("You can ask me about loans, interest rates, credit reports, and more.")

    user_input = st.text_input("You:", "")
    if st.button("Send"):
        if user_input:
            prompt = f"As a FinTech expert, please provide a concise explanation: {user_input}"
            response = get_response(prompt)
            st.text_area("Chatbot:", value=response, height=200)

if __name__ == "__main__":
    main()
