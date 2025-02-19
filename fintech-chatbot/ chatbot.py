import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def fintech_chatbot(user_input):
    # Define the system message to set the context
    system_message = """
    You are a financial assistant for a FinTech company. Your expertise includes loans, interest rates, credit reports, CIBIL scores, and other financial services. 
    Provide clear, concise, and accurate answers to user queries.
    """

    # Combine the system message and user input
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ]

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=messages,
        max_tokens=150,  # Limit response length
        temperature=0.7  # Control creativity (0 = strict, 1 = creative)
    )

    # Extract and return the chatbot's response
    return response['choices'][0]['message']['content']