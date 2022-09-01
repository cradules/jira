# Import the request HTTP library for python
# Documentation http://docs.python-requests.org/en/master/user/quickstart/
import requests
# Import HTTPBasicAuth to handle the required authentication for the web services
from requests.auth import HTTPBasicAuth
# Import json library to process encoding and decoding of JSON responses
import json
import os
from jira import JIRA
import sqlite3
import os

data_dir = "sql_app.db"

con = sqlite3.connect(data_dir, check_same_thread=False)
cur = con.cursor()

HOST_URL = os.getenv('HOST_URL')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
PROJECT_ID = os.getenv('PROJECT_ID')

jira = JIRA(server=HOST_URL, basic_auth=(USER, PASSWORD))


def connection_db(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE items
              SET linked_issues = ?
              WHERE issue_id = ? '''
    cur.execute(sql, task)
    conn.commit()


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


# issues = jira.search_issues('project=REQSDLC')
# issues_list = []
# for issue in issues:
#     print(issue.fields.issuetype)
#     issues_list.append(issue.fields.issuetype)
# print(issues_list)

# Update DB "linked_issue" column
# def update_issue_link():
#     shrs = cur.execute("SELECT issue_id FROM items WHERE issue_type != 'Business Requirements'")
#     for shr in shrs:
#         issue_id = jira.issue(shr[0])
#         issue_links = issue_id.fields.issuelinks
#         # print(issue_id)
#         for link in issue_links:
#             if hasattr(link, "outwardIssue"):
#                 outwardIssue = link.outwardIssue
#                 outwardIssue_type = link.type.outward
#                 print(outwardIssue_type)
#                 if 'part of requirement' in str(outwardIssue_type):
#                     # print(issue_id, outwardIssue)
#                     c = con.cursor()
#                     c.execute('UPDATE items SET linked_issues = ? WHERE issue_id = ?', (str(outwardIssue), str(issue_id)))
#                     c.fetchall()
#
#
# update_issue_link()


#
def id_field(field_name):
    fields = jira.fields()

    for f in fields:
        if f['name'] == field_name:
            return f['id']


#
#
# screens = jira.screens()
#
#
# print(screens[0])


# def update_br_specific_id(filed_name):
#     cur.execute(f"SELECT issue_id FROM items WHERE issue_type = '{}'")
#     queries = cur.fetchall()
#     for query in queries:
#         cur.execute('SELECT package FROM items WHERE issue_id = ?', query)
#         package_raw = cur.fetchall()
#         package = package_raw[0][0]
#         issue = jira.issue(query)
#         field_id = id_field(filed_name)
#         issue.update(fields={field_id: package})

#
# def update_pkg_db_other(req_type):
#     cur.execute(f"SELECT issue_id FROM items WHERE issue_type == '{req_type}'")
#     queries = cur.fetchall()
#     print(queries)
#     i = 0
#     for query in queries:
#         print(query)
#         cur.execute('SELECT linked_issues FROM items WHERE issue_id = ?', query)
#         br_id_raw = cur.fetchall()
#         br_id = br_id_raw[0]
#         cur.execute('SELECT package FROM items WHERE issue_id = ?', br_id)
#         package_raw = cur.fetchall()
#         i = i + 1
#         package = str(package_raw[0][0]) + "." + str(i)
#         cur.execute(f"UPDATE items SET package = '{package}' where issue_id = '{query[0]}'")
#     con.commit()

# def update_other_id_jira(req_type, field_name):
#     cur.execute(f"SELECT issue_id FROM items where issue_type = '{req_type}'")
#     issues_db_id = cur.fetchall()
#     print(issues_db_id)
#     for issue_db_id in issues_db_id:
#         cur.execute('SELECT package FROM items WHERE issue_id = ?', issue_db_id)
#         package_raw = cur.fetchall()
#         package = package_raw[0][0]
#         issue_raw = issue_db_id[0]
#         issue = jira.issue(issue_raw)
#         field_id = id_field(field_name)
#         issue.update(fields={field_id: package})
#         print('Filed "{}" with ID {} for issue with ID {} has been updated' .format(field_name, field_id, issue_db_id[0]))


# update_other_id_jira('Stakeholder Requirements', 'RP Specific ID')
# update_pkg_db("Business Requirements")
# update_pkg_db_other("Stakeholder Requirements")
# update_pkg_db_other("Functional Requirements")
# update_pkg_db_other("Non-Functional requirements")
# def update_db_issue_link(req_type):
#     shrs = cur.execute(f"SELECT issue_id FROM items WHERE issue_type = '{req_type}'")
#     for shr in shrs:
#         issue_id = jira.issue(shr[0])
#         issue_links = issue_id.fields.issuelinks
#         for link in issue_links:
#             if hasattr(link, "outwardIssue"):
#                 outwardIssue = link.outwardIssue
#                 outwardIssue_type = link.type.outward
#                 print(outwardIssue_type)
#                 print("\tOutward: " + outwardIssue.key)
#                 if 'part of requirement' in str(outwardIssue_type):
#                     query = f"UPDATE items SET linked_issues = '{outwardIssue}' WHERE issue_id = '{issue_id}'"
#                     print(query)
#                     c = con.cursor()
#                     c.execute(query)
#                     c.fetchall()
#         con.commit()
#
# update_db_issue_link('Non-Functional requirements')
