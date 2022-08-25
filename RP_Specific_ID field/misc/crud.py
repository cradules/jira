# Import the request HTTP library for python
# Documentation http://docs.python-requests.org/en/master/user/quickstart/
import requests
# Import HTTPBasicAuth to handle the required authentication for the web services
from requests.auth import HTTPBasicAuth
# Import json library to process encoding and decoding of JSON responses
import json
import os
from sqlalchemy.orm import Session
from misc import models
from database import SessionLocal

HOST_URL = os.getenv('HOST_URL')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
PROJECT_ID = os.getenv('PROJECT_ID')


def get_requirements_path_for_issues(host_url, username, password, jql):
    """
    This method is used to get all requirements path for all issues returned by a jql
    Template parameters:
    [jql] the JQL statement
    """

    # The REST API path to search for tree elements
    path_uri = '/rest/com.easesolutions.jira.plugins.requirements/1.0/issue/req-path/' + jql

    # Send a GET request to get all requirements path for all issues returned by a jql
    # Return the result of the GET
    try:
        return requests.get(host_url + path_uri, auth=HTTPBasicAuth(username, password))
    except requests.exceptions.RequestException as e:
        print(e)


def create_item(db: Session, project_id):
    # ['project = REQ'] jql parameter to get the parent issue keys
    response = get_requirements_path_for_issues(HOST_URL, USER, PASSWORD, f'project = {project_id}')
    print(response)

    # Check response if requirements path are found
    if response.status_code == 200:

        # Get the value of the JSON response and print in a readable JSON format
        # json dumps formats the JSON string in readable format
        json_object = json.loads(response.text)

        # Iterate trough all objects and extract the db_elements
        # Declare global variables
        count = 0
        issue_id = []
        issue_type = []
        pkg = []
        while count < len(json_object):
            # Extract the path of the objects
            paths = json_object[count]['paths']
            # Identify the key of the object (issue)
            issue_id = json_object[count]['issueKey']
            # Check if the path is populated
            if paths:
                # Extract the package number
                # Check if RP is part of the path
                if 'RP' in str(paths[0]['path']):
                    # Extract the package number
                    txt = paths[0]['path'][1].split()
                    txt = txt[0].split('.')
                    pkg = txt[1]
                    issue_type = paths[0]['path'][0]
                    db_elements = models.Item(project_id=project_id, issue_id=issue_id, issue_type=issue_type, package=pkg)
                    db.add(db_elements)
                    db.commit()
                    db.refresh(db_elements)
                    # return db_elements
            count += 1
    else:
        print('Error code: ', response.status_code)
        print(response.text)
