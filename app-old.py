import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from openai import OpenAI

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# setup an OpenAI client
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

def get_sql_query():
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
            "role": "system",
            "content": "You are an expert in converting English questions to SQL query!"
                   "The SQL database has a table name CREW_MEMEBR and has the following columns - crewProfileId, crewId,firstName,lastName, "
                   "dob,dateOfJoin,dateOfContract,crewType,status"
                   "\n\nFor example,\nExample 1 - How many active crew member are present?, "
                   "the SQL command will be something like this SELECT COUNT(*) FROM CREW_MEMEBR where status='1' ;"
                   "\nExample 2 - Give me all active captains?, "
                   "the SQL command will be something like this SELECT * FROM CREW_MEMEBR where crewType='OC' "
                   "also the sql code should not have ``` in beginning or end and sql word in output"
            },
            *st.session_state.messages
        ],
        temperature=0,
        top_p=1
    )

    return response

#Setup the Chat APP

st.title("Rostering Planning Assistant")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container    
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    
    # getting the response
    response = get_sql_query();

    # Extracting the response message
    response_message = response.choices[0].message.content
    print(response)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response_message)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_message})



