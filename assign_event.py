import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import json
from apicalls import RequestHandler
import sqlite3
from datetime import datetime

apiHandler = RequestHandler()

load_dotenv()

baseUrl = 'api url'
headers = {}

def assign_event(self,crewProfileId,eventId,days):       
    #implement the API
    post_response = {}
    return post_response

def assign(input_prompt):
    print("assign event")
    client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": 
                "You are an expert extraction algorithm. "
                "Only extract relevant information from the text. "
                "If you do not know the value of an attribute asked to extract, "
                "return null for the attribute's value."

                "Please consider following event Description"
                "[{\"event_id\":63,\"eventCode\":'ABC',\"eventDescription\": \"Absent\"},"
                "{\"event_id\":9,\"eventCode\":'ALV',\"eventDescription\": \"Annual Leave\"}"
                "{\"event_id\":67,\"eventCode\":'CCTS',\"eventDescription\": \"Cabin Crew Training Supervisor duty\"},"
                "{\"event_id\":7,\"eventCode\":'OFF',\"eventDescription\": \"Day Off\"},"
                "]"

                "Some examples:"

                "Example 01"
                "Input: Assign ALV to crew id 1631 for the dates between 25/03/2024 and 26/03/2024 dates"
                "Output: event='ALV' crewId=1631 dates=['25/03/2024','26/03/2024]'"

                "If you do not know any of required fields, Please ask requried details from user dont call any funcation and continue the general conversation"
            },
            {"role":"user","content":input_prompt}
        ],
        functions= [
            {
                "name": "extract_assign_event_details",
                "description": "extract the given detail from promt. If required data not available should return null. data should extract based on the user promt only",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "event": {
                            "type": "string",
                            "description": "The Event Code ex :ALV",
                        },
                        "eventId": {
                            "type": "number",
                            "description": "The Event Id ex :9",
                        },
                        "crewId": {
                            "type": "number",
                            "description": "Crew ID ex:1631",
                        },
                        "dates": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Dates in array ex : ['25/03/2024','26/03/2024]",
                        },
                        
                    },
                    "required": ["event", "eventId","crewId","dates"],
                },
            }
        ]
    )
    json_response = json.loads(completion.choices[0].message.function_call.arguments)
    print(json_response)
    # if json_response['event'] =='ALV' : 
    #     eventId = 9
    sql_query = f"SELECT crewProfileId FROM CREW_ROASTERY_MASTER WHERE crewId = '{json_response['crewId']}'"

    connection=sqlite3.connect(os.getenv("DB_NAME"))
    cursor=connection.cursor()

    print(sql_query)

    data =cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
   
    crew_profile_id = 0
    for row in rows:
        print(row)
        crew_profile_id = row[0]  
        print(crew_profile_id)
    apiresponse = apiHandler.assign_event(crew_profile_id,json_response['eventId'],json_response['dates'])

    dates = json_response['dates']
    
    dates = [datetime.strptime(date, '%d/%m/%Y') for date in dates]

    # Find minimum and maximum dates
    min_date = min(dates)
    max_date = max(dates)

    # Convert back to string format
    min_date_str = min_date.strftime('%d/%m/%Y')
    max_date_str = max_date.strftime('%d/%m/%Y')


    #search_crew_roster(str(json_response['crewId']),"CP",min_date_str,max_date_str)

    jsonApiresponse = json.loads(apiresponse)
    if "\"success\": true" in apiresponse:
        return "Assign successfull"
    else:
        return "Failed to Assign"

def unassign(input_prompt):
    print("unassign event")
    client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": 
                "You are an expert extraction algorithm. "
                "Only extract relevant information from the text. "
                "If you do not know the value of an attribute asked to extract, "
                "return null for the attribute's value."

                "Some examples:"

                "Example 01"
                "Input: UnAssign crew id 1631 between 25/03/2024 and 26/03/2024 dates"
                "Output: crewIds=['1631'] dates=['25/03/2024','26/03/2024]'"

                "Example 02"
                "Input: UnAssign crew id 1631,1632 between 25/03/2024 and 26/03/2024 dates"
                "Output: crewIds=['1631','1632'] dates=['25/03/2024','26/03/2024]'"

                "Example 03"
                "Input:Assign OFF to crew id 102161 on 22/03/2024"
                "Output: crewIds=['102161'] dates=['22/03/2024']"

                "If you do not know any of required fields, Please ask requried details from user dont call any funcation and continue the general conversation"
            },
            {"role":"user","content":input_prompt}
        ],
        functions= [
            {
                "name": "extract_unassign_event_details",
                "description": "extract the given detail from promt",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "crewIds": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Crew ID ex:['1631','1632']",
                        },
                        "dates": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Dates in array ex : ['25/03/2024','26/03/2024']",
                        },
                        
                    },
                    "required": ["origin"],
                },
            }
        ]
    )
    json_response = json.loads(completion.choices[0].message.function_call.arguments)
    print(json_response)

    # Extract crewIds and dates from the data dictionary
    crew_ids = json_response['crewIds']
    dates = json_response['dates']

    # Convert list elements to string format with single quotes for SQL
    crew_ids_str = ', '.join("'" + str(id) + "'" for id in crew_ids)
    dates_str = ', '.join("'" + str(date) + "'" for date in dates)

    print(dates)

    dates = [datetime.strptime(date, '%d/%m/%Y') for date in dates]

    # Find minimum and maximum dates
    min_date = min(dates)
    max_date = max(dates)

    # Convert back to string format
    min_date_str = min_date.strftime('%d/%m/%Y')
    max_date_str = max_date.strftime('%d/%m/%Y')

    # Construct SQL query with IN statement
    sql_query = f"SELECT D.crewProfileId,D.crewScheduleBlockId FROM CREW_ROASTERY_DETAILS D inner join CREW_ROASTERY_MASTER M ON D.crewProfileId=M.crewProfileId WHERE M.crewId IN ({crew_ids_str}) AND D.checkinDate BETWEEN '{min_date_str}' AND '{max_date_str}'"

    print(sql_query)

    connection=sqlite3.connect(os.getenv("DB_NAME"))
    cursor=connection.cursor()

    data =cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    result = []
    for row in rows:
        crew_profile_id = row[0]  # Assuming crewProfileId is the first column in your query result
        crew_schd_block_id = row[1]  # Assuming crewSchdBlockId is the second column in your query result
        result.append({"crewProfileId": crew_profile_id, "crewSchdBlockId": crew_schd_block_id})

    print(result)
    apiresponse = apiHandler.remove_event(result)
    jsonApiresponse = json.loads(apiresponse)
    if "\"success\": true" in apiresponse:
        return "Unassign successfull"
    else:
        return "Failed to Unassign"

def swap_duties(input_prompt):
    print("swap duties")
    client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": 
                "You are an expert extraction algorithm. "
                "Only extract relevant information from the text. "
                "If you do not know the value of an attribute asked to extract, "
                "return null for the attribute's value."

                "Some examples:"

                "Example 01"
                "Input: Swap duties on day 30/03/2024 between crew id 2327 and 1475"
                "Output: crewIds=['2327','1475'] date='30/03/2024'"

                "If you do not know any of required fields, Please ask requried details from user dont call any funcation and continue the general conversation"
            },
            {"role":"user","content":input_prompt}
        ],
        functions= [
            {
                "name": "extract_swap_duties_details",
                "description": "extract the given detail from promt",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "crewIds": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Crew ID ex:['123','456']",
                        },
                        "date": {
                            "type": "string",
                            "description": "Date ex:'25/03/2024'",
                        },
                        
                    },
                    "required": ["origin"],
                },
            }
        ]
    )
    json_response = json.loads(completion.choices[0].message.function_call.arguments)
    print(json_response)

    # Extract crewIds and dates from the data dictionary
    crew_ids = json_response['crewIds']
    date = json_response['date']

    # Convert list elements to string format with single quotes for SQL
    crew_ids_str = ', '.join("'" + str(id) + "'" for id in crew_ids)
    #dates_str = ', '.join("'" + str(date) + "'" for date in dates)

    # Construct SQL query with IN statement
    sql_query = f"SELECT D.crewProfileId,D.crewScheduleBlockId,M.crewType FROM CREW_ROASTERY_DETAILS D INNER JOIN CREW_ROASTERY_MASTER M ON D.crewProfileId=M.crewProfileId WHERE D.crewProfileId IN ({crew_ids_str}) AND D.checkinDate = '{date}'"

    
    print(sql_query)

    connection=sqlite3.connect(os.getenv("DB_NAME"))
    cursor=connection.cursor()

    data =cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    result = []
    
    for index,row in enumerate(rows):
        crew_profile_id = row[0]  # Assuming crewProfileId is the first column in your query result
        crew_schd_block_id = row[1]  # Assuming crewSchdBlockId is the second column in your query result
        crew_type = row[2]  # Assuming crewSchdBlockId is the second column in your query result
        if index == 0 :
            result.append({"owner": crew_profile_id,"shiftTo":int(crew_ids[1]), "crewSchdBlockId": crew_schd_block_id,"crewType":crew_type})
        if index == 1 :
            result.append({"owner": crew_profile_id,"shiftTo":int(crew_ids[0]), "crewSchdBlockId": crew_schd_block_id,"crewType":crew_type})
    
    print(result)
    #{\"owner\":1,\"shiftTo\":2\"crewSchdBlockId\":1123,\"crewType\":'CP'}

    # swapcompletion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": 
    #             "You are an expert swaping given json details. "
    #             "Only Swaping the relevent details between the elements"

    #             "Some examples:"

    #             "Example 01"
    #             "Input Json : [{\"crewProfileId\":1,\"crewSchdBlockId\":1123,\"crewType\":'CP'},"
    #             "{\"crewProfileId\":2,\"crewSchdBlockId\":2345,\"crewType\":'CP'},"
    #             "{\"crewProfileId\":3,\"crewSchdBlockId\":3456,\"crewType\":'CP'}]"
    #             "Output: [{\"owner\":1,\"shiftTo\":2\"crewSchdBlockId\":1123,\"crewType\":'CP'},"
    #             "{\"owner\":2,\"shiftTo\":3\"crewSchdBlockId\":2345,\"crewType\":'CP'},"
    #             "{\"owner\":3,\"shiftTo\":1\"crewSchdBlockId\":3456,\"crewType\":'CP'}]"

    #             "Example 02"
    #             "Input Json : [{\"crewProfileId\":1,\"crewSchdBlockId\":1123,\"crewType\":'CP'},"
    #             "{\"crewProfileId\":2,\"crewSchdBlockId\":2345,\"crewType\":'CP'}]"
    #             "Output: [{\"owner\":1,\"shiftTo\":2\"crewSchdBlockId\":1123,\"crewType\":'CP'},"
    #             "{\"owner\":2,\"shiftTo\":1\"crewSchdBlockId\":2345,\"crewType\":'CP'}]"

    #             "If you do not know any of required fields, Please ask requried details from user dont call any funcation and continue the general conversation"
    #         },
    #         {"role":"user","content":result}
    #     ],
    #     functions= [
    #         {
    #             "name": "swap_duties_details",
    #             "description": "swap the details from given input",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "owner": {
    #                         "type": "string",
    #                         "description": "Crew Id of the Owner ex:1",
    #                     },
    #                     "shiftTo": {
    #                         "type": "string",
    #                         "description": "Crew Id of the Swaping with ex:2",
    #                     },
    #                     "crewSchdBlockId": {
    #                         "type": "string",
    #                         "description": "crewSchdBlockId of the owner schedule ex:'1123'",
    #                     },
    #                     "crewType": {
    #                         "type": "string",
    #                         "description": "Crew type of the Owner ex:'1'",
    #                     },
    #                 },
    #                 "required": ["origin"],
    #             },
    #         }
    #     ]
    # )
    # print("swapin llm")
    #json_response = json.loads(swapcompletion.choices[0].message.function_call.arguments)
    #print(json_response)
    apiresponse=apiHandler.swap_duties(result)
    jsonApiresponse = json.loads(apiresponse)
    if jsonApiresponse['success'] :
        return "Duties have been successfully swapped"
    else:
        return "Failed to swap"

def assign_duties(input_prompt):
    print("assign duties")
    client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": 
                "You are an expert extraction algorithm. "
                "Only extract relevant information from the text. "
                "If you do not know the value of an attribute asked to extract, "
                "return null for the attribute's value."

                "Some examples:"

                "Example 01"
                "Input: Assign duty  SHJ-KTM/RS /KTM-SHJ-22:40 on 24/03/2024 to crewID 1601"
                "Output: duty='SHJ-KTM/RS /KTM-SHJ-22:40' date='24/03/2024' crewIds=['1601']"

                "If you do not know any of required fields, Please ask requried details from user dont call any funcation and continue the general conversation"
            },
            {"role":"user","content":input_prompt}
        ],
        functions= [
            {
                "name": "extract_assign_duties_details",
                "description": "extract the given detail from promt",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "duty": {
                            "type": "string",
                            "description": "duty name ex:'SHJ-KTM/RS /KTM-SHJ-22:40'",
                        },
                        "date": {
                            "type": "string",
                            "description": "Date ex:'25/03/2024'",
                        },
                        "crewIds": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Crew ID ex:['123','456']",
                        },
                    },
                    "required": ["duty","date","crewId"],
                },
            }
        ]
    )
    json_response = json.loads(completion.choices[0].message.function_call.arguments)
    print(json_response)

    # Extract crewIds and dates from the data dictionary
    duty = json_response['duty']
    date = json_response['date']
    #crewId = json_response['crewId']

    crew_ids = json_response['crewIds']

    # Convert list elements to string format with single quotes for SQL
    crew_ids_str = ', '.join("'" + str(id) + "'" for id in crew_ids)
    #dates_str = ', '.join("'" + str(date) + "'" for date in dates)

    # Construct SQL query with IN statement
    sql_query = f"SELECT crewProfileId,crewId FROM CREW_ROASTERY_MASTER where crewId in ({crew_ids_str})"

    print(sql_query)

    connection=sqlite3.connect(os.getenv("DB_NAME"))
    cursor=connection.cursor()

    data = cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    result = []
    crew_profile_id = 0
    for row in rows:
        crew_profile_id = row[0]  # Assuming crewProfileId is the first column in your query result
        crewId = row[1]
        apiresponse=apiHandler.search_assignable_duties(crew_profile_id,date)
        print("response here")
        #print(json.loads(apiresponse))
        jsonres = json.loads(apiresponse)
        #print(jsonres)
        #print(jsonres['patternDTOs'])

        print(len(jsonres['patternDTOs']))

        if jsonres['success']  and len(jsonres['patternDTOs']) > 0:
            filtered_objects = [obj for obj in jsonres['patternDTOs'] if duty in obj['patternName']]

        if len(filtered_objects) > 0 :

            assignres = apiHandler.assign_duty(crew_profile_id,filtered_objects[0]['patternId'])
        
            jsonres = json.loads(assignres)
            if jsonres['success'] :
                result.append({"CrewId":crewId,"Status":"The Duty Has been Assigned Successfully"})
            else:
                error = "The Duty Assign Failed"
                for key, value in jsonres["regulationMap"].items():
                    for val in value:
                        error = error + val['description']
                result.append({"CrewId":crewId,"Status":error})
        else :
            result.append({"CrewId":crewId,"Status":"Duty Not Found"})

        return result
        
def post_request(url, headers, data):
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        # Parse JSON response
        response_json = response.json()
        json_string = json.dumps(response_json)
        return json_string
    else:
        # Handle error
        return ""

def get_request(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse JSON response
        response_json = response.json()
        json_string = json.dumps(response_json)
        return json_string
    else:
        # Handle error
        return ""
    
def get_crew_types_master():       
    url = '/commonService/crew/types'
    post_response = get_request(baseUrl + url, headers=headers)
    print('POST Response:', post_response)
    return post_response

def get_crew_master():       
    url = '/commonService/search/crew'
    data = {'crewType': '','active': 'true'}
    post_response = post_request(baseUrl + url, headers=headers, data=data)
    print('POST Response:', post_response)
    return post_response





def search_crew_roster(crewIds, crewTypes, fromDate, toDate):
    print("search_crew_roster")
        
    conn = sqlite3.connect(os.getenv("DB_NAME"), timeout=10)
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute("SELECT crewId, crewType FROM CREW_ROASTERY_MASTER WHERE crewProfileId = ?", (crewIds,))
    

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Convert the rows to a list of dictionaries
    result = []
    crewId =''
    crewType = ''
    for row in rows:
        crewId = row[0]
        crewType = row[1]
        #result.append({'crewId': row[0], 'crewType': row[1]})

    # Convert the result to JSON
    
    # Close the cursor and connection
    cursor.close()
    conn.close()

    print(result)
    url = '/crewingService/search/quick/schedules'
    data = {
        "crewIds": crewId,
        "crewType": crewType,
        "fromDate": fromDate,
        "toDate": toDate,
    }
    print(data)

    post_response = post_request(baseUrl + url, headers=headers, data=data)
    
    if not post_response:
        print("No response or empty response received.")
    

    try:
        json_data = json.loads(post_response)
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    

    crew_ndto_data = []
    crew_rostery_details_data = []

    for data in json_data["crewScheduleNewDTOs"]:
        for duty in data["rosterDutyNewDTOs"]:
            duty["crewProfileId"] = data["crewNDTO"]["crewProfileId"]

    crew_ndto_data = []
    crew_roasterydetails_data = []
    for crewScheduleNewDTO in json_data['crewScheduleNewDTOs']:
        crew_ndto_data.append(crewScheduleNewDTO['crewNDTO'])
        crew_roasterydetails_data.append(crewScheduleNewDTO['rosterDutyNewDTOs'])

    crew_ndto_json = {
        "crewScheduleNewDTOs": [{"crewNDTO": crew_ndto} for crew_ndto in crew_ndto_data]
    }

    crew_roasterydetails_json = {
        "crewScheduleNewDTOs": [{"rosterDutyNewDTOs": crew_ndto} for crew_ndto in crew_roasterydetails_data]
    }

    isUpdate = False
    string_array = []
    if crewIds == '':
        isUpdate = False 

    else:
        isUpdate = True
        string_array = crewIds.split(",")
    

    insert_roastery_master(crew_ndto_json,isUpdate)
    insert_roastery_details(crew_roasterydetails_json,isUpdate)

    responseSummary = search_crew_flying_hours(fromDate,toDate,crewTypes,string_array)
    
    insert_roastery_summary(responseSummary,isUpdate)

    insert_roaster_main()

    


def search_crew_flying_hours(fromDate,toDate,crewType,crewIds):       
    url = '/crewingService/search/flightAndCreditHours'
    data = {
                "startDate": fromDate,
                "endDate": toDate,
                "crewType": crewType,
                "crewIds": crewIds
            }
    post_response = post_request(baseUrl + url, headers=headers, data=data)
    json_data = json.loads(post_response)
    for key, value in json_data["flightAndCreditHoursDtoMap"].items():
        value["crewProfileId"] = int(key)
    
    
    return json_data

def insert_roastery_master(json_data,isupdate):
    conn = sqlite3.connect(os.getenv("DB_NAME"), timeout=10)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ROASTERY_MASTER (
        crewProfileId INTEGER,
        crewId TEXT,
        firstName TEXT,
        lastName TEXT,
        crewType TEXT,
        flyingDuration INTEGER,
        dutyDuration INTEGER,
        offCount INTEGER,
        nightCount INTEGER,
        gender TEXT,
        modelNumbers TEXT,
        layoverCount INTEGER
    )
    ''')

    # Insert data into the table
    if isupdate:
        for crew in json_data['crewScheduleNewDTOs']:
            crew_data = crew['crewNDTO']
            cursor.execute('''
                UPDATE ROASTERY_MASTER
                SET crewId = ?,
                    firstName = ?,
                    lastName = ?,
                    crewType = ?,
                    flyingDuration = ?,
                    dutyDuration = ?,
                    offCount = ?,
                    nightCount = ?,
                    gender = ?,
                    modelNumbers = ?,
                    layoverCount = ?
                WHERE crewProfileId = ?
            ''', (
                crew_data['crewId'],
                crew_data['firstName'],
                crew_data['lastName'],
                crew_data['crewType'],
                crew_data['flyingDuration'],
                crew_data['dutyDuration'],
                crew_data['offCount'],
                crew_data['nightCount'],
                crew_data['gender'],
                crew_data['modelNumbers'],
                crew_data['layoverCount'],
                crew_data['crewProfileId']
            ))
    else:            
        for crew in json_data['crewScheduleNewDTOs']:
            crew_data = crew['crewNDTO']

            cursor.execute("SELECT COUNT(*) FROM ROASTERY_MASTER WHERE crewProfileId = ?", (crew_data['crewProfileId'],))
            count = cursor.fetchone()[0]                
            if count > 0:
                
                cursor.execute('''
                UPDATE ROASTERY_MASTER
                SET crewId = ?,
                    firstName = ?,
                    lastName = ?,
                    crewType = ?,
                    flyingDuration = ?,
                    dutyDuration = ?,
                    offCount = ?,
                    nightCount = ?,
                    gender = ?,
                    modelNumbers = ?,
                    layoverCount = ?
                WHERE crewProfileId = ?
            ''', (
                crew_data['crewId'],
                crew_data['firstName'],
                crew_data['lastName'],
                crew_data['crewType'],
                crew_data['flyingDuration'],
                crew_data['dutyDuration'],
                crew_data['offCount'],
                crew_data['nightCount'],
                crew_data['gender'],
                crew_data['modelNumbers'],
                crew_data['layoverCount'],
                crew_data['crewProfileId']
            ))
            else:
                cursor.execute('''
                INSERT INTO ROASTERY_MASTER
                (crewProfileId, crewId, firstName, lastName, crewType, flyingDuration, dutyDuration, offCount, nightCount, gender, modelNumbers, layoverCount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    crew_data['crewProfileId'],
                    crew_data['crewId'],
                    crew_data['firstName'],
                    crew_data['lastName'],
                    crew_data['crewType'],
                    crew_data['flyingDuration'],
                    crew_data['dutyDuration'],
                    crew_data['offCount'],
                    crew_data['nightCount'],
                    crew_data['gender'],
                    crew_data['modelNumbers'],
                    crew_data['layoverCount']
                ))

    # Commit the inserts
    conn.commit()
    conn.close()

def insert_roastery_details(json_data,isupdate):        
    # Connect to the SQLite database
    conn = sqlite3.connect(os.getenv("DB_NAME"), timeout=10)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CREW_ROASTERY_DETAILS (
        crewScheduleBlockId INTEGER,
        patternId INTEGER,
        blockId INTEGER,
        checkInDate TEXT,
        checkInTime TEXT,
        checkOutDate TEXT,
        checkOutTime TEXT,
        blockName TEXT,
        patternName TEXT,
        fontColor TEXT,
        backColor TEXT,
        blockLegal TEXT,
        auto INTEGER,
        manual INTEGER,
        request INTEGER,
        blockType TEXT,
        minRest INTEGER,
        signed INTEGER,
        acmiViolated INTEGER,
        bluelineCrew INTEGER,
        paxMessageRejected INTEGER,
        targetHoursValid INTEGER,
        crewProfileId INTEGER
    )
    ''')

    if isupdate:
            for crew_schedule in json_data['crewScheduleNewDTOs']:
                for roster_duty in crew_schedule['rosterDutyNewDTOs']:
                    cursor.execute('''
                        UPDATE CREW_ROASTERY_DETAILS
                        SET
                            patternId = ?,
                            blockId = ?,
                            checkInDate = ?,
                            checkInTime = ?,
                            checkOutDate = ?,
                            checkOutTime = ?,
                            blockName = ?,
                            patternName = ?,
                            fontColor = ?,
                            backColor = ?,
                            blockLegal = ?,
                            auto = ?,
                            manual = ?,
                            request = ?,
                            blockType = ?,
                            minRest = ?,
                            signed = ?,
                            acmiViolated = ?,
                            bluelineCrew = ?,
                            paxMessageRejected = ?,
                            targetHoursValid = ?
                        WHERE crewProfileId = ?
                    ''', (
                        roster_duty['patternId'],
                        roster_duty['blockId'],
                        roster_duty['checkInDate'],
                        roster_duty['checkInTime'],
                        roster_duty['checkOutDate'],
                        roster_duty['checkOutTime'],
                        roster_duty['blockName'],
                        roster_duty['patternName'],
                        roster_duty['fontColor'],
                        roster_duty['backColor'],
                        roster_duty['blockLegal'],
                        roster_duty['auto'],
                        roster_duty['manual'],
                        roster_duty['request'],
                        roster_duty['blockType'],
                        roster_duty['minRest'],
                        roster_duty['signed'],
                        roster_duty['acmiViolated'],
                        roster_duty['bluelineCrew'],
                        roster_duty['paxMessageRejected'],
                        roster_duty['targetHoursValid'],
                        roster_duty['crewProfileId']
                    ))
    else:
    # Insert data into the table
        for crew_schedule in json_data['crewScheduleNewDTOs']:
            for roster_duty in crew_schedule['rosterDutyNewDTOs']:
                cursor.execute("SELECT COUNT(*) FROM CREW_ROASTERY_DETAILS WHERE crewScheduleBlockId = ?", (roster_duty['crewScheduleBlockId'],))
                count = cursor.fetchone()[0]
                if count > 0:
                    cursor.execute('''
                    UPDATE CREW_ROASTERY_DETAILS
                    SET
                        patternId = ?,
                        blockId = ?,
                        checkInDate = ?,
                        checkInTime = ?,
                        checkOutDate = ?,
                        checkOutTime = ?,
                        blockName = ?,
                        patternName = ?,
                        fontColor = ?,
                        backColor = ?,
                        blockLegal = ?,
                        auto = ?,
                        manual = ?,
                        request = ?,
                        blockType = ?,
                        minRest = ?,
                        signed = ?,
                        acmiViolated = ?,
                        bluelineCrew = ?,
                        paxMessageRejected = ?,
                        targetHoursValid = ?
                    WHERE crewScheduleBlockId = ?
                ''', (
                    roster_duty['patternId'],
                    roster_duty['blockId'],
                    roster_duty['checkInDate'],
                    roster_duty['checkInTime'],
                    roster_duty['checkOutDate'],
                    roster_duty['checkOutTime'],
                    roster_duty['blockName'],
                    roster_duty['patternName'],
                    roster_duty['fontColor'],
                    roster_duty['backColor'],
                    roster_duty['blockLegal'],
                    roster_duty['auto'],
                    roster_duty['manual'],
                    roster_duty['request'],
                    roster_duty['blockType'],
                    roster_duty['minRest'],
                    roster_duty['signed'],
                    roster_duty['acmiViolated'],
                    roster_duty['bluelineCrew'],
                    roster_duty['paxMessageRejected'],
                    roster_duty['targetHoursValid'],
                    roster_duty['crewScheduleBlockId']
                ))
                else:
                    
                    cursor.execute('''
                    INSERT INTO CREW_ROASTERY_DETAILS
                    (crewScheduleBlockId, patternId, blockId, checkInDate, checkInTime, checkOutDate, checkOutTime, blockName, patternName, fontColor, backColor, blockLegal,
                    auto, manual, request, blockType, minRest, signed, acmiViolated, bluelineCrew, paxMessageRejected, targetHoursValid, crewProfileId)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        roster_duty['crewScheduleBlockId'],
                        roster_duty['patternId'],
                        roster_duty['blockId'],
                        roster_duty['checkInDate'],
                        roster_duty['checkInTime'],
                        roster_duty['checkOutDate'],
                        roster_duty['checkOutTime'],
                        roster_duty['blockName'],
                        roster_duty['patternName'],
                        roster_duty['fontColor'],
                        roster_duty['backColor'],
                        roster_duty['blockLegal'],
                        roster_duty['auto'],
                        roster_duty['manual'],
                        roster_duty['request'],
                        roster_duty['blockType'],
                        roster_duty['minRest'],
                        roster_duty['signed'],
                        roster_duty['acmiViolated'],
                        roster_duty['bluelineCrew'],
                        roster_duty['paxMessageRejected'],
                        roster_duty['targetHoursValid'],
                        roster_duty['crewProfileId']
                    ))

    # Commit the inserts
    conn.commit()

    # Close the connection
    conn.close()

def insert_roastery_summary(json_data,isupdate):
    conn = sqlite3.connect(os.getenv("DB_NAME"), timeout=10)
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS ROASTERY_SUMMARY
                (id INTEGER PRIMARY KEY,
                crewId TEXT,
                creditHrs TEXT,
                flightHrs INTEGER,
                nightCount INTEGER,
                offCount INTEGER,
                leaveCount INTEGER,
                nightDepartureCount INTEGER,
                fourOrMoreSectorCount INTEGER,
                layoverCount INTEGER,
                crewProfileId INTEGER)''')

    # Insert records into the table
    if isupdate:
        for key, value in json_data['flightAndCreditHoursDtoMap'].items():
            cursor.execute('''
                UPDATE ROASTERY_SUMMARY
                SET
                    crewId = ?,
                    creditHrs = ?,
                    flightHrs = ?,
                    nightCount = ?,
                    offCount = ?,
                    leaveCount = ?,
                    nightDepartureCount = ?,
                    fourOrMoreSectorCount = ?,
                    layoverCount = ?
                WHERE crewProfileId = ?
            ''', (
                value['crewId'],
                value['creditHrs'],
                value['flightHrs'],
                value['nightCount'],
                value['offCount'],
                value['leaveCount'],
                value['nightDepartureCount'],
                value['fourOrMoreSectorCount'],
                value['layoverCount'],
                value['crewProfileId']
            ))
    else:
        for key, value in json_data['flightAndCreditHoursDtoMap'].items():
            cursor.execute("SELECT COUNT(*) FROM ROASTERY_SUMMARY WHERE crewProfileId = ?", (value['crewProfileId'],))
            count = cursor.fetchone()[0]
            if count > 0:
                cursor.execute('''
                UPDATE ROASTERY_SUMMARY
                SET
                    crewId = ?,
                    creditHrs = ?,
                    flightHrs = ?,
                    nightCount = ?,
                    offCount = ?,
                    leaveCount = ?,
                    nightDepartureCount = ?,
                    fourOrMoreSectorCount = ?,
                    layoverCount = ?
                WHERE crewProfileId = ?
            ''', (
                value['crewId'],
                value['creditHrs'],
                value['flightHrs'],
                value['nightCount'],
                value['offCount'],
                value['leaveCount'],
                value['nightDepartureCount'],
                value['fourOrMoreSectorCount'],
                value['layoverCount'],
                value['crewProfileId']
            ))
            else:
                cursor.execute('''INSERT INTO ROASTERY_SUMMARY 
                                (crewId, creditHrs, flightHrs, nightCount, offCount, leaveCount, nightDepartureCount, fourOrMoreSectorCount, layoverCount, crewProfileId) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (value['crewId'], value['creditHrs'], value['flightHrs'], value['nightCount'], value['offCount'], value['leaveCount'], value['nightDepartureCount'], value['fourOrMoreSectorCount'], value['layoverCount'], value['crewProfileId']))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def insert_roaster_main():
    conn = sqlite3.connect(os.getenv("DB_NAME"), timeout=10)
    cursor = conn.cursor()

    # Create a new table using a SELECT query

    cursor.execute('DROP TABLE IF EXISTS CREW_ROASTERY_MASTER')

    cursor.execute('''CREATE TABLE IF NOT EXISTS CREW_ROASTERY_MASTER AS
                    SELECT RSM.crewProfileId, RSM.crewId, RSM.firstName, RSM.lastName, RSM.crewType, RSM.flyingDuration, RSM.dutyDuration, RSM.gender, RSM.modelNumbers, RS.creditHrs, RS.flightHrs, RS.nightCount, RS.offCount, RS.leaveCount, RS.nightDepartureCount, RS.fourOrMoreSectorCount, RS.layoverCount
                    FROM ROASTERY_MASTER RSM 
                    LEFT JOIN ROASTERY_SUMMARY RS ON RSM.crewProfileId = RS.crewProfileId''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()