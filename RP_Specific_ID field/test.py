# Import the request HTTP library for python
# Documentation http://docs.python-requests.org/en/master/user/quickstart/
import requests
# Import HTTPBasicAuth to handle the required authentication for the web services
from requests.auth import HTTPBasicAuth
# Import json library to process encoding and decoding of JSON responses
import json
import os
from jira import JIRA

HOST_URL = os.getenv('HOST_URL')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
PROJECT_ID = os.getenv('PROJECT_ID')

jira = JIRA(server=HOST_URL, basic_auth=(USER, PASSWORD))


# Read r4j API https://easesolutions.atlassian.net/wiki/spaces/REQ4J/pages/73433185/Get+Requirement+version
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


# response = get_requirements_path_for_issues(HOST_URL, USER, PASSWORD, 'project = REQ')
#
# # Check response if requirements path are found
# if response.status_code == 200:
#
#     # Get the value of the JSON response and print in a readable JSON format
#     # json dumps formats the JSON string in readable format
#     json_object = json.loads(response.text)
#     print(json_object)
#     count = 0
#     issue = []
#     while count < len(json_object):
#         paths = json_object[count]['paths']
#         issue_id = json_object[count]['issueKey']
#         if paths:
#             print(issue_id)
#             print(paths[0]['path'][0])
#         count += 1
# else:
#     print('Error code: ', response.status_code)
#     print(response.text)


issues = jira.search_issues('project=REQSDLC')
issues_list = []
for issue in issues:
    print(issue.fields.issuetype)
    issues_list.append(issue.fields.issuetype)
print(issues_list)
