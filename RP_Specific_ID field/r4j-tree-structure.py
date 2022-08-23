# Import the request HTTP library for python
# Documentation http://docs.python-requests.org/en/master/user/quickstart/
import requests

# Import HTTPBasicAuth to handle the required authentication for the web services
from requests.auth import HTTPBasicAuth

# Import json library to process encoding and decoding of JSON responses
import json

HOST_URL = "https://jira.sdlcpoc.eu"
USER = "radulescuc"
PASSWORD = "p3thbiAsFeqbgJBJ"
PROJECT = "REQSDLC"


# Function to get complete tree structure

def get_project_tree(host_url, username, password, project_key, n):
    """
    This method is used to search for tree elements
    Template parameters:
    [project_key] the project key
    Query parameters:
    [element_path] the path to search in
    """

    # The REST API path to search for tree elements
    path_uri = '/rest/com.easesolutions.jira.plugins.requirements/1.0/tree/' + project_key + '?'

    # The field-value pair/s that will be added to the query string
    number_prefix_field_value = 'n=' + str(n)

    # The query string to be added to the URI
    query_string = number_prefix_field_value

    # Send a GET request to search for tree elements
    # Return result of the GET request
    try:
        return requests.get(host_url + path_uri + query_string, auth=HTTPBasicAuth(username, password))
    except requests.exceptions.RequestException as e:
        print(e)


# Function to print folder structure
def print_folder_structure(folders):
    # If folder has values then print the information of the folder
    if folders:
        print('\n%s %s' % ('Display name: ', folders[0]['name_display']))
        print('%s %s' % ('Folder ID: ', folders[0]['id']))
        print('%s %s' % ('Parent folder ID: ', folders[0]['parent']))

        # Perform recursion if there is a folder under this folder
        sub_folders = folders[0]['folders']
        print_folder_structure(sub_folders)


response = get_project_tree(HOST_URL, USER, PASSWORD, PROJECT, 1)

# Check response if element info is returned
if response.status_code == 200:

    # Get the value of the JSON response
    # Pass the result to print_folder_structure method to print the folder structure of the found element
    json_object = json.loads(response.text)
    folders = json_object['folders']
    print_folder_structure(folders)

else:
    print('Error code: ', response.status_code)
    print(response.text)
