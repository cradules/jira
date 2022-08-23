
from jira import JIRA

# "After we had a discussion about this request we have reach the next conclusion:
#
#  ID = SDL-REQ will be taken from the ID project
#
# 02 = Take it from R4j tree
# as mandatory
#
# 12 = Check what BR are under the packge and start number them wih 01 and increment
# when should be incremented and when not?
#
# 35 = represents the SHR and always will be incremented with 1. This will be linked by user with BR.
#
#
#
# BR > SHRs > FRs/NFRs"

# Example

# BR = SQLREQ-01
# SHR = SQLREQ-01-01
# FR/NFR = SQLREQ-01-01-01

HOST_URL = "https://jira.sdlcpoc.eu"
USER = "radulescuc"
PASSWORD = "p3thbiAsFeqbgJBJ"
# By default, the client will connect to a Jira instance started from the Atlassian Plugin SDK
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
jira = JIRA(basic_auth=(USER, PASSWORD), options={'server': HOST_URL})

# Get all projects
projects = jira.projects()

# print(projects)

projects_id = []
project_name = []

print(projects)

# for project in projects:
#     projects_id.append(project.id)
#     project_name.append(project)
#
# print(project_name)


def list_issues(project_id):
    for single_issue in jira.search_issues(jql_str=f'project = {project_id}'):
        print('{}: {}: {}:{}'.format(single_issue.key, single_issue.fields.issuetype, single_issue.fields.summary,
                                     single_issue.fields.reporter.displayName))


def list_br_key(project_id, issue_type):
    br_list = []
    for single_issue in jira.search_issues(jql_str=f'project = {project_id}'):
        if issue_type == str(single_issue.fields.issuetype):
            br_list.append(str(single_issue.key))
    return br_list


def issues_link(project_id, issue_type):
    for single_issue in jira.search_issues(jql_str=f'project = {project_id}'):
        list_link = []
        if issue_type == str(single_issue.fields.issuetype):
            list_link.append(single_issue.fields.issuelinks)
        return list_link


# for issue_key in list_br_key(10101, "Business Requirement"):
#     singleIssue = jira.issue(issue_key)
#     print('{}: {}: {}:{}: {}'.format(singleIssue.key, singleIssue.fields.issuetype,
#                                      singleIssue.fields.summary,
#                                      singleIssue.fields.reporter.displayName, singleIssue.fields.issuelinks))


