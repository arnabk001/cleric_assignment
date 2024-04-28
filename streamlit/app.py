import streamlit as st
import requests


st.title('Fact Extraction from Multiple Call Logs')

# User inputs
question = st.text_input("Enter your question:")
urls_input = st.text_input("Enter URLs (comma-separated):")

if st.button('Extract Facts'):
    if urls_input and question:
        # Split the input by commas to handle multiple URLs
        urls = urls_input.split(',')
        post_qdoc_response = requests.post("http://18.226.180.95:8000/submit_question_and_documents", 
                                          json = {"question": question, "documents":urls})
        if post_qdoc_response.ok:
            ## the returned text 
            response = requests.get("http://18.226.180.95:8000/get_question_and_facts")
            if response.status_code == 200:
                facts = response.json()
                st.text_area("Extracted facts", value="\n".join(f"- {item}" for item in facts["facts"]), help="Displays the extracted facts")
            else:
                st.error("Failed to retrieve facts")
        else:
            st.error("Failed to post inputs")
    elif not urls_input:
        st.error("Please enter at least one URL.")
    else:
        st.error("Please enter the question.")

