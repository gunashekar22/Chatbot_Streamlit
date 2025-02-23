import json
import streamlit as st
from meta_ai_api import MetaAI
from fuzzywuzzy import process  # For better question matching

# Initialize MetaAI
ai = MetaAI()

# Load predefined questions
with open('questions.json', 'r') as file:
    dataset = json.load(file)

# Convert questions to lowercase for case-insensitive matching
questions_responses = [{"question": item["question"].lower(), "response": item["response"]} for item in dataset]

# Function to find best response using fuzzy matching
def find_response(user_query):
    best_match, score = process.extractOne(user_query.lower(), [qa["question"] for qa in questions_responses])

    # If confidence is high, return corresponding response
    if score > 75:  # Adjust threshold as needed
        return next(qa["response"] for qa in questions_responses if qa["question"] == best_match)
    return None  # No close match found

# Function to query MetaAI if no match is found
def get_meta_ai_response(user_query):
    dataset_string = json.dumps(dataset)
    prompt_message = f"Use only the given dataset to answer the question. Do not make up answers.\nDataset: {dataset_string}\nQuestion: {user_query}"
    
    response = ai.prompt(message=prompt_message)
    return response.get('message', "I'm sorry, I couldn't find an answer for that question.")

# Logging function
def log_question_and_response(question, response):
    with open("all_questions_answers.txt", "a") as log_file:
        log_file.write(f"Question: {question}\nResponse: {response}\n\n")

# Streamlit chatbot UI
def chatbot():
    st.title("Chatbot Application")
    st.write("Chatbot is ready! Type your question below.")
    
    user_query = st.text_input("You:", "")

    if user_query:
        response = find_response(user_query)
        
        
        if response:
            st.write("Chatbot:", response)
        else:
            st.write("Chatbot: I'm consulting my knowledge base, please wait...")
            response = get_meta_ai_response(user_query)

            # Ensure response is valid
            if response:
                st.write("Chatbot:", response)
            else:
                st.write("Chatbot: I'm sorry, I couldn't find an answer for that question.")
        
        log_question_and_response(user_query, response)




if __name__ == "__main__":
    chatbot()
