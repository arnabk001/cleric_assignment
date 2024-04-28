from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel, HttpUrl

import requests
from openai import OpenAI

## main functions ##########################################

# function to fetch URl text
def fetch_and_concatenate_texts(urls):
    """ Fetches texts from a list of URLs and concatenates them. """
    all_texts = []
    for url in urls:
        try:
            response = requests.get(str(url).strip())
            response.raise_for_status()  # will raise an HTTPError for bad responses
            all_texts.append(response.text)
        except requests.RequestException as e:
            all_texts.append(f"Failed to fetch data from {url}: {e}")
    return "\n\n".join(all_texts)

# define openai call for text processing
def extract_facts(text, question):
    openai_key = 'YOUR-API-KEY'
    client = OpenAI(api_key=openai_key)

    system_msg = """you are an expert in information extraction from call logs and present a final list of facts to answer the user query \n
                    you will be given a single user question along with a list of call logs. You will present facts as a bulleted list, using simple and clear language.
                    you should process the documents (i.e. call logs) to extract facts relevant to the question. Remember that Document ordering matters. 
                    A later document may modify the fact from the initial conversation. So initial logs may introduce new facts, but the facts in later logs may
                    - Add new facts to the list of facts OR - Change facts in the list of facts OR - Remove facts in the list of facts. \n
                    for example, if on day one a fact is “We should use red on our landing page”, then if the team decides “We shouldn't have a landing page”, 
                    then the previous fact about using red on the landing page should not exist any more in the final list of facts. \n
                    You have to optimize your answer for accuracy. \n \n
                    Here is a complete example:\n
                    user query = "What are our product design decisions?" \n
                    here is the text provided by the user: \n
                    "
                    1
                    00:01:11,430 --> 00:01:40,520
                    John: I've been thinking about our decision on the responsive design. While it's important to ensure our product works well on all devices, I think we should focus on desktop first. Our primary users will be using our product on desktops.
                    2
                    00:01:41,450 --> 00:01:49,190
                    Sara: I see your point, John. Focusing on desktop first will allow us to better cater to our primary users. I agree with this change.
                    3
                    00:01:49,340 --> 00:01:50,040
                    Mike: I agree as well. I also think the idea of using a modular design doesn't make sense. Let's not make that decision yet.
                    "\n\n
                    the expected answer is:\n
                    - The team has decided to focus on a desktop-first design
                    - The team has decided to provide both dark and light theme options for the user interface.
                """
    prompt = f"""here is the user question you have to answer:\n f{question} \n \n
                 here are the user provided call logs: \n f{text} \n    
                 \n
                 extract and present a final list of facts (extracted from these call logs) as per the following guidelines:\n
                 - You must not have unnecessary facts
                 - Your list of facts must not have duplicate facts (two facts per line)
                 - the order of calls changes the list of facts (e.g, the final call is the most important since its the most recent)
              """

    messages = [{"role": "system", "content": system_msg},
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
                                model="gpt-4",
                                messages=messages,
                                )

    generated_texts = response.choices[0].message.content.split(" - ")
    return generated_texts

#######################################################################################
# MAIN APP
#######################################################################################

app = FastAPI()

total_text = ""
question = ""

class GetQuestionAndFactsResponse(BaseModel):
    question: str
    facts: List[str]
    status: str

class SubmitQuestionAndDocumentsRequest(BaseModel):
    question: str
    documents: List[HttpUrl]

@app.post("/submit_question_and_documents")
async def submit_qdoc(request_data: SubmitQuestionAndDocumentsRequest) -> dict:
    try:
        global total_text, question
        # Extract the URLs from the request data
        urls = request_data.documents
        question = request_data.question
        # Call the asynchronous fetch function
        total_text = fetch_and_concatenate_texts(urls)
        return {"message": "Processing started", "status": "accepted"}
    except Exception as e:
        # Log or handle the error accordingly
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_question_and_facts")
async def get_qf() -> GetQuestionAndFactsResponse:
    try:
        global question, total_text
        # Extract facts based on global variables
        facts = extract_facts(total_text, question)
        # Check if processing is done and set status accordingly
        status = "done" if facts else "processing"
        # Create response object
        return GetQuestionAndFactsResponse(question=question, facts=facts, status=status)
    except Exception as e:
        # Log or handle the error accordingly
        raise HTTPException(status_code=500, detail=str(e))
