import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
#from openai import OpenAI
#from langchain import OpenAI
#from langchain_community.llms import OpenAI
from langchain.agents import load_tools,Tool,initialize_agent,AgentType,create_openai_functions_agent
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

from TextToSql import text_to_sql

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


llm = ChatOpenAI(
    openai_api_key=os.getenv("OPEN_API_KEY"),
    temperature=0
)

def assign_alv(input_promt):
    return  "Assign ALv"

def extract_details(input_promt):
    return "Extract the Details"

def swap_duties(input_promt):
    return "Swap Duties"


tools = [
    Tool(
        name="text_to_sql",
        func=text_to_sql,
        description="Converting English questions to SQL query"
    ),
    Tool(
        name="extract_details",
        func=extract_details,
        description="extraction algorithm. "
    ),
    Tool(
        name="assign_alv",
        func=assign_alv,
        description="Assign ALV"
    ),
    Tool(
        name="swap_duties",
        func=swap_duties,
        description="Swap Duties"
    )
]


assistant_agent = create_openai_functions_agent(
    tools,
    llm,
    verbose=True,
    max_iterations=10
)



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
    response =assistant_agent(prompt);

    print(response)

    # Extracting the response message
    response_message = response['output']
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response_message)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_message})


