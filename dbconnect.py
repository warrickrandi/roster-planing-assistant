import os
from dotenv import load_dotenv
load_dotenv()
import sqlite3
import json

## Connectt to SQlite
connection=sqlite3.connect(os.getenv("DB_NAME"))
cursor=connection.cursor()


## create the table
table_info="""
CREATE TABLE IF NOT EXISTS CREW_MEMBER (
    crewProfileId INT,
    crewId VARCHAR(10),
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    dob DATE,
    dateOfJoin DATE,
    dateOfContract DATE,
    crewType VARCHAR(50),
    status int
);
"""


cursor.execute(table_info)

