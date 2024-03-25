# import os
# from dotenv import load_dotenv
# load_dotenv()
# import streamlit as st
# from openai import OpenAI
# #from dbconnect import connection, cursor
# import re
# import json
# import sqlite3


# connection=sqlite3.connect(os.getenv("DB_NAME"))
# cursor=connection.cursor()

# # setup an OpenAI client
# client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))


# def read_sql_query(responseoutput):
#     print(responseoutput.choices[0].message.content)
#     # Define regular expression patterns for SQL statements
#     # sql_patterns = {
#     #     'SELECT': r'\bSELECT\b.*?(?=\bFROM\b|$)',
#     #     'INSERT': r'\bINSERT\b.*?(?=\bINTO\b|$)',
#     #     'UPDATE': r'\bUPDATE\b.*?(?=\bSET\b|$)',
#     #     'DELETE': r'\bDELETE\b.*?(?=\bFROM\b|$)'
#     # }
#     #data=cursor.execute(responseoutput.choices[0].message.content)
#     data =cursor.execute("SELECT * FROM CREW_MEMBER WHERE crewType='CP' AND status='1'")
#     for row in data:
#         print(row)
#     return data
#     # # Extract and print SQL statements
#     # for sql_type, pattern in sql_patterns.items():
#     #     sql_match = re.search(pattern, responseoutput.choices[0].message.content, re.IGNORECASE | re.DOTALL)
#     #     if sql_match:
#     #         query = sql_match.group().strip()
#     #         print(query)
#     #         data=cursor.execute(query)
#     #         for row in data:
#     #             print(row)
#     #         return data
#     #     else : 
#     #         return {'input': '', 'output': "Given Details are not Proper"}

# def text_to_sql(input_promt):
#     print("Calling the text to sql from texttosql page")
#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=[
#             {
#             "role": "system",
#             "content": "You are an expert in converting English questions to SQL query!"
#                    "The SQL database has a below tables"
#                    "\n\nTable name CREW_MEMBER and has the following columns - crewProfileId, crewId,firstName,lastName, "
#                    "dob,dateOfJoin,dateOfContract,crewType,status"
#                    "\nTable name CREW_TYPE and has following columns - crewTypeId,crewType,status"
#                    "\nTable Name ROASTERY_MASTER and has following columns -crewProfileId, crewId, firstName, lastName, crewType, "
#                    "flyingDuration, dutyDuration, offCount, nightCount, gender, modelNumbers, layoverCount,crewId,creditHrs,flightHrs,"
#                    "nightCount,offCount,leaveCount,nightDepartureCount,fourOrMoreSectorCount"
#                    "\nTable Name CREW_ROASTERY_DETAILS and has follwing columns crewScheduleBlockId, patternId, blockId, checkInDate," 
#                    "checkInTime,checkOutDate, checkOutTime, blockName, patternName, fontColor,backColor, blockLegal, auto, manual,"
#                    "request, blockType, minRest,signed, acmiViolated, bluelineCrew, paxMessageRejected, targetHoursValid,crewProfileId"
#                    "\n\nTable Connections are below"
#                    "CREW_TYPE table crewType is crewType of all tables"
#                    "\nROASTERY_MASTER crewProfileId is the foreign key of the CREW_ROASTERY_DETAILS crewProfileId"
#                    "\n\n\nDefiantion for the CrewType as follow CP - Captain, FO - First Officer, CS - Cabin Supervisor, CC - Cabin Crew"
#                    "\n as a Example if user mention as Captain you need to take crewType as 'CP'"
#                    "\n\nYour job is converting English questions to SQL Quey"
#                    "\n\nFor example,\nExample 1 - How many active crew member are present?, "
#                    "the SQL command will be something like this SELECT COUNT(*) FROM CREW_MEMBER where status='1' ;"
#                    "\nExample 2 - Give me all active captains?, "
#                    "the SQL command will be something like this SELECT * FROM CREW_MEMBER where crewType='OC' "
#                    "\nExample 3 - show me the G9 CP that have less than 4 nights, flying hours are below range, "
#                    "500 -600 and leave count more than 10. "
#                    "the SQL command will be something like this select * from ROASTERY_MASTER where crewType='CP' and "
#                    "nightCount < 4 and flightHrs >= 500 and flightHrs <=600 and leaveCount > 10 "
#                    "also the sql code should not have ``` in beginning or end and sql word in output"
#                    "Please give the exact sql query without any prefix, if you can not create the query return as null"
#             },
#             {
#                 "role":"user",
#                 "content" : input_promt
#             }
#         ],
#         temperature=0,
#         top_p=1
#     )
#     return read_sql_query(response)

