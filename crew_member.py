import os
import json
from dbconnect import connection, cursor

# Read JSON data from file

base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the JSON file
json_file_path = os.path.join(base_dir, 'Data', 'crew_list.json')

with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

# Function to check if crew member exists
def crew_member_exists(crew_profile_id):
    cursor.execute("SELECT COUNT(*) FROM CREW_MEMBER WHERE crewProfileId = ?", (crew_profile_id,))
    count = cursor.fetchone()[0]
    return count > 0

# Insert data into the table
for crew_member in json_data['crewList']:
    profile_id = crew_member['crewProfileId']
    if not crew_member_exists(profile_id):
        cursor.execute('''
            INSERT INTO CREW_MEMBER (crewProfileId, crewId, firstName, lastName, dob, dateOfJoin, dateOfContract, crewType, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?
                    )
        ''', (
            crew_member['crewProfileId'],
            crew_member['crewId'],
            crew_member['firstName'],
            crew_member['lastName'],
            crew_member['dob'],
            crew_member['dateOfJoin'],
            crew_member['dateOfContract'],
            crew_member['crewType'],
            1
        ))

# data=cursor.execute('''Select * from CREW_MEMBER''')
# for row in data:
#     print(row)

query = "SELECT * FROM CREW_MEMBER WHERE crewType='CP' AND status='1'"
data=cursor.execute(query)
for row in data:
    print(row)

# Commit the transaction and close the connection
connection.commit()
connection.close()
