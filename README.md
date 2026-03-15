# job-application-assistant

I built this tool to make job applications easier. You paste a job description and it automatically analyzes it against my CV, tells you how well it matches, what skills are missing, and writes a cover letter for you.

## Why I built this

Applying for jobs takes a lot of time. I wanted something that could instantly tell me how suitable I am for a role and save me the effort of writing a cover letter from scratch every time.

## How it works

You paste a job description into the Streamlit interface and click Analyze. The app sends it to an n8n workflow through a webhook. The AI Agent then searches my CV data stored in Pinecone, compares it with the job description using Groq, and returns three things: a match score, a list of missing skills, and a generated cover letter.

## Tech Stack

n8n for workflow automation, Pinecone as the vector database, Cohere for embeddings, Groq as the AI model, and Streamlit for the frontend.

## How to Run

Install the required library using pip install streamlit requests, then add your webhook URL in app.py, and run it with python -m streamlit run app.py.

## How to Import the Workflow

Open n8n, click Add Workflow, select Import from File, choose the workflow.json file, and add your own API credentials for Pinecone, Cohere and Groq.
