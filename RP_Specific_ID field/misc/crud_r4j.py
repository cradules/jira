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
import sqlite3
from jira import JIRA

HOST_URL = os.getenv('HOST_URL')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
PROJECT_ID = os.getenv('PROJECT_ID')

# Create instance for jira API, using jira python library
jira = JIRA(server=HOST_URL, basic_auth=(USER, PASSWORD))


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


def create_items(db: Session, project_id):
    # Clear data before import new one, since is just temporary to avoid any conflicts or "dirty data".
    db_items = []
    conn = sqlite3.connect('sql_app.db')
    c = conn.cursor()
    c.execute('DELETE FROM items;', )
    conn.commit()
    conn.close()

    # Generate HTTP API response from R4J API
    issues_by_jira_search = jira.search_issues(f'project={project_id}')
    response = get_requirements_path_for_issues(HOST_URL, USER, PASSWORD, f'project = {project_id}')

    # Check response if requirements path are found
    if response.status_code == 200:

        # Get the value of the JSON response and print in a readable JSON format
        # json dumps formats the JSON string in readable format
        json_object = json.loads(response.text)

        # Iterate trough all objects and extract the db_elements
        # Declare global variables
        count = 0
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
                    db_items = models.Item(project_id=project_id, issue_id=issue_id, issue_type=issue_type, package=pkg)
                    db.add(db_items)
                    db.commit()
                    db.refresh(db_items)
                elif 'RP' not in str(paths[0]['path']):
                    issue_type = paths[0]['path'][0]
                    db_items = models.Item(project_id=project_id, issue_id=issue_id, issue_type=issue_type)
                    db.add(db_items)
                    db.commit()
                    db.refresh(db_items)

            count += 1
    return db_items


