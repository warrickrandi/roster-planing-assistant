import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent,Tool
from langchain import hub
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from dbconnect import connection, cursor
import sqlite3
from langchain_core.prompts import ChatPromptTemplate

connection=sqlite3.connect(os.getenv("DB_NAME"))
cursor=connection.cursor()

#from TextToSql import text_to_sql
from openai import OpenAI

from assign import Assign

from assign_event import assign,unassign,swap_duties,assign_duties


# setup an OpenAI client
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

def fetch_sql_query(responseoutput):
    print("read sql")
    print(responseoutput)
    #sprint(responseoutput.choices[0].message.content)
    data =cursor.execute(responseoutput)
    rows = cursor.fetchmany(20)
    connection.commit()
    for row in rows:
        print(row)
    return rows

def diplay_db_result(data):
    print("display the result")
    return data

def text_to_sql(input_promt):
    print("Calling the text to sql from texttosql page")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
            "role": "system",
            "content": "You are an expert in converting English questions to SQL query!"
                       "The SQL database has a below tables and should not use any other table other than defined"
                       "\n\nTable name CREW_MEMBER and has the following columns - crewProfileId, crewId,firstName,lastName, "
                        "dob,dateOfJoin,dateOfContract,crewType,status"
                        "\nTable name CREW_TYPE and has following columns - crewTypeId,crewType,status"
                        "\nTable Name CREW_ROASTERY_MASTER and has following columns -crewProfileId, crewId, firstName, lastName, crewType, "
                        "flyingDuration, dutyDuration, offCount, nightCount, gender, modelNumbers, layoverCount,creditHrs,flightHrs,"
                        "nightCount,offCount,leaveCount,nightDepartureCount,fourOrMoreSectorCount,layoverCount:1"
                        "\nTable Name CREW_ROASTERY_DETAILS and has follwing columns crewScheduleBlockId, patternId, blockId, checkInDate," 
                        "checkInTime,checkOutDate, checkOutTime, blockName, patternName, fontColor,backColor, blockLegal, auto, manual,"
                        "request, blockType, minRest,signed, acmiViolated, bluelineCrew, paxMessageRejected, targetHoursValid,crewProfileId"
                        "\n\nFor Crew Member Master details such as name,should target CREW_ROASTERY_MASTER table"
                        "\n\nTable Connections are below"
                        "CREW_TYPE table crewType is crewType of all tables"
                        "For the Crew details need to use the CREW_ROASTERY_MASTER table"
                        "\nCREW_ROASTERY_MASTER crewProfileId is the foreign key of the CREW_ROASTERY_DETAILS crewProfileId"
                       "\n\n\Definition for the CrewType as follow CP - Captain, FO - First Officer, CS - Cabin Supervisor, CC - Cabin Crew"
                       "\n\n\Definition for the gender as follow M - Male, F - Female"
                       "\n\n YOu need target flying hours CREW_ROASTERY_MASTER table flightHrs for Flight Hours"
                       "\n as a Example if user mention as Captain you need to take crewType as 'CP'"
                       "\n\nYour job is converting English questions to SQL Quey"
                       "\n\nFor example,\nExample 1 - How many active crew member are present?, "
                       "the SQL command will be something like this SELECT COUNT(*) FROM CREW_MEMBER where status='1' ;"
                       "\nExample 2 - Give me all active captains?, "
                       "the SQL command will be something like this SELECT crewId, crewNumber, firstName, lastName, dateOfBirth, joinDate, resignDate, crewType, status FROM CREW_MEMBER where crewType='OC' "
                       "\nExample 3 - show me the G9 CP that have less than 4 nights, flying hours are below range, "
                       "500 -600 and leave count more than 10. "
                       "the SQL command will be something like this select crewProfileId, crewId, firstName, lastName, crewType, flyingDuration, dutyDuration, offCount, nightCount, gender, modelNumbers, layoverCount from ROASTERY_MASTER where crewType='CP' and "
                       "nightCount < 4 and flightHrs >= 500 and flightHrs <=600 and leaveCount > 10 "
                       "\nExample 4 - show me the G9 CP that have target hours higher than 51"
                       "the SQL command will be something like this SELECT crewProfileId, firstName, lastName, crewType, targetHoursValid FROM CREW_ROASTERY_DETAILS WHERE crewType='CP' AND targetHoursValid > 51"
                       "also the sql code should not have ``` in beginning or end and sql word in output"
                       "Please give the exact sql query without any prefix, if you can not create the query return as null"
                       "for select queries please use column name to fetch instead of all(*) and all columns should fetch. Shoul use available columns which was defined"
                       "Please join the table when ever required by defined table connections"
                       "Dont use not available columns for the query"
            },
            {
                "role":"user",
                "content" : input_promt
            }
        ],
        temperature=0,
        top_p=1
    )
    return response


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        # HumanMessage(role='user',content="hi!"),
        AIMessage(role='system',content="Hello! How can I assist you today?")
    ]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPEN_API_KEY"),
    temperature=0
)

# def assign_alv(input_promt):
#     print("assign alv")
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": 
#                 "You are an expert extraction algorithm. "
#                 "Only extract relevant information from the text. "
#                 "If you do not know the value of an attribute asked to extract, "
#                 "return null for the attribute's value."

#                 "Some examples:"

#                 "Example 01"
#                 "Input: I want to go to paris"
#                 "Output: origin='null' destination='Paris' date='null'"

#                 "Example 02"
#                 "Input: I want to go to colombo from sharjah on 2021/2/1"
#                 "Output: origin='sharjah' destination='colombo' date='2021/2/1'"

#                 "Example 03"
#                 "Input: From colombo"
#                 "Output: origin='colombo' destination='null' date='null'"

#                 "If you do not know any of required fields, Please ask requried details from user dont call any funcation and continue the general conversation"
#             },
#             {"role":"user","content":"I need travel to Sharjah"}
#         ],
#         functions= [
#             {
#                 "name": "extract_flight_details",
#                 "description": "extract the given detail from promt",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "origin": {
#                             "type": "string",
#                             "description": "The Depature Airport ex: CMB",
#                         },
#                         "destination": {
#                             "type": "string",
#                             "description": "The Arriaval Airport ex: CMB",
#                         },
#                         "date": {
#                             "type": "string",
#                             "description": "Travel Date ex : 2023/04/02",
#                         },
                        
#                     },
#                     "required": ["origin"],
#                 },
#             }
#         ]
#     )
#     extractllm = ChatOpenAI(openai_api_key=os.getenv("OPEN_API_KEY"),model="gpt-3.5-turbo", temperature=0)
#     runnable = extraction_prompt | extractllm.with_structured_output(schema=Assign)
#     # response = runnable.invoke({"text": input_promt})
#     # print(response)
#     return  "Assign Alv"

# def assign_event(input_promt):
#     return  "Assign Event"

# def extract_details(input_promt):
#     print("extract details")
#     return "Extract the Details"

# def swap_duties(input_promt):
#     print("swap duties")
#     return "Swap Duties"


tools = [
    Tool(
        name="text_to_sql",
        func=text_to_sql,
        description="Converting English questions to SQL query"
    ),
    Tool(
        name="fetch_sql_query",
        func=fetch_sql_query,
        description="execute the extract sql and fetch data from db return the db result"
    ),
    Tool(
        name="diplay_db_result",
        func=diplay_db_result,
        description="display the fetched data set with all fields header"
    ),
    Tool(
        name="assign",
        func=assign,
        description="Assign"
    ),
    Tool(
        name="unassign",
        func=unassign,
        description="unassign"
    ),
    Tool(
        name="assign_duty",
        func=assign_duties,
        description=""
    ),
    # Tool(
    #     name="return",
    #     func=read_sql_query,
    #     description="execute the extract sql get query result from db and display the result list as a json"
    # )
    # Tool(
    #     name="extract_details",
    #     func=extract_details,
    #     description="extraction algorithm. "
    # ),
    
    Tool(
        name="swap_duties",
        func=swap_duties,
        description="Swap Duties"
    )
]


agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)


#Setup the Chat APP

st.title("Crew Mate")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message.role):
        st.markdown(message.content)

# React to user input
if user_input := st.chat_input("What is up?"):
    # Display user message in chat message container    
    st.chat_message("user").markdown(user_input)
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(role='user',content=user_input))

    
    # getting the response
    response = agent_executor.invoke({"input": user_input})

    print(response)

    # Extracting the response message
    response_message = response['output']
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response_message)
    # Add assistant response to chat history
    st.session_state.messages.append(AIMessage(role='system',content=response_message))

connection.close()


