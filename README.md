# Cleric Assignment

## Overview
The Cleric Assignment is a web application designed to process user queries using a combination of Streamlit for the frontend and FastAPI for the backend. This README outlines the project structure, functionality, and key design aspects.

## Architecture
- **Frontend**: Developed using Streamlit, the frontend allows users to input a question and multiple URLs.
- **Backend**: Built with FastAPI, the backend processes these inputs, fetches and processes text from the URLs, and interacts with the OpenAI ChatGPT-4 API.
- **Hosting**: Defined docker containers for both streamlit and fast-api, hosted using AWS EC2 instance.

## Key Functionalities
1. **User Input Handling**: The frontend collects a question and multiple URLs from the user.
2. **Data Processing**: The backend uses FastAPI to:
   - Retrieve text from the provided URLs.
   - Concatenate the text into a single block.
3. **Interaction with ChatGPT-4**: The processed text and the user's question are sent to the ChatGPT-4 API, which returns the relevant answer.
4. **Response**: The response from ChatGPT-4 is then sent back to the frontend and displayed to the user.

## Design Aspects
- **Global Variables**: Utilized to store the user's question and the concatenated text from URLs.
- **Efficient URL Processing**: All URLs are processed simultaneously to optimize response time.
- **Prompt Engineering**: Careful prompt engineering ensures that the concatenated text and user's question are effectively used by ChatGPT-4 to generate accurate and relevant responses.

## Installation and Setup
To run this project locally:
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Use docker to build the repo
   ```bash
   docker-compose build
   ```
3. Run in detached mode:
   ```bash
   docker-compose run --detached
   ```

## License
This project is released under the MIT License. For more details, see the LICENSE file in the repository.
