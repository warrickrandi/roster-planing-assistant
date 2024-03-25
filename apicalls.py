import requests
import json
from flask import jsonify
from datetime import datetime, timedelta


class RequestHandler:
    
    baseUrl = 'http://roater-management-api'
    headers = {'Content-Type': 'application/json', 'token-id': ''}
    
    def __init__(self):
        pass

    def post_request(self, url, headers, data):
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            # Parse JSON response
            response_json = response.json()
            json_string = json.dumps(response_json)
            return json_string
        else:
            # Handle error
            response_json = response.json()
            json_string = json.dumps(response_json)
            return json_string

    def get_request(self, url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Parse JSON response
            response_json = response.json()
            json_string = json.dumps(response_json)
            return json_string
        else:
            # Handle error
            response_json = response.json()
            json_string = json.dumps(response_json)
            return json_string
        
    def get_crew_types_master(self):       
        url = '/commonService/crew/types'
        post_response = self.get_request(self.baseUrl + url, headers=self.headers)
        print('POST Response:', post_response)
        return post_response
    
    def get_crew_master(self):  
        #implement the search api
        post_response = {'crewIds': '','crewType': 'true'}
        return post_response
    
    def search_crew_roster(self,crewIds,crewTypes,fromDate,toDate):       
        #implement the API
        post_response = {}
        return post_response
    
    
    def search_crew_flying_hours(self,fromDate,toDate,crewType,crewIds):       
        #implement the API
        post_response = {}
        return post_response
    
    
    def assign_event(self,crewProfileId,eventId,days):       
        #implement the API
        post_response = {}
        return post_response
    
    def swap_duties(self,crewDuties):       
        #implement the API
        post_response = {}
        return post_response

    def remove_event(self,crewDuties):       
        #implement the API
        post_response = {}
        return post_response
    
    def search_assignable_duties(self,crewProfileId, date):       
        #implement the API
        post_response = {}
        return post_response
    
    def assign_duty(self,crewProfileId, patternId):       
        #implement the API
        post_response = {}
        return post_response
  
