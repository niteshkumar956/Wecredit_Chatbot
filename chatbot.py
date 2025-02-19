import streamlit as st
import google.generativeai as genai  # Correct import
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API key from .env file
api_key = os.getenv("API_KEY")

# Initialize the API key (correct method)
genai.configure(api_key=api_key)

def get_response(prompt):
    try:
        # Generate content using Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")  # Use correct model name
        response = model.generate_content(prompt)

        # Return the generated text
        return response.text if hasattr(response, "text") else "No response generated."
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
