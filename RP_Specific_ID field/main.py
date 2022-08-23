import re
from jira import JIRA

# "After we had a discussion about this request we have reach the next conclusion:
#
#  ID = SDL-REQ will be taken from the ID project
#
# 02 = represents package number and will be provided by the user. We need to create a costume field "Package number"
# as mandatory
#
# 12 = represents the BR and will be given by the automation process. This must increment.  Here is the question,
# when should be incremented and when not?
#
# 35 = represents the SHR and always will be incremented with 1.
#
#
#
# BR > SHRs > FRs/NFRs"


# By default, the client will connect to a Jira instance started from the Atlassian Plugin SDK
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
jira = JIRA(basic_auth=("radulescuc", "p3thbiAsFeqbgJBJ"), options={'server': "https://jira.sdlcpoc.eu"})

# Get all projects
projects = jira.projects()

# print(projects)

projects_id = []
project_name = []


# for project in projects:
#     projects_id.append(project.id)
#     project_name.append(project)
#
# print(project_name)


# def list_issues(project_id):
#     for singleIssue in jira.search_issues(jql_str=f'project = {project_id}'):
#         print('{}: {}: {}:{}'.format(singleIssue.key, singleIssue.fields.issuetype, singleIssue.fields.summary,
#                                      singleIssue.fields.reporter.displayName))
#
#
# list_issues(10101)


def list_br_key(project_id, issue_type):
    br_list = []
    for single_issue in jira.search_issues(jql_str=f'project = {project_id}'):
        if issue_type == str(single_issue.fields.issuetype):
            br_list.append(str(single_issue.key))
    return br_list


for issue_key in list_br_key(10101, "Business Requirement"):
    singleIssue = jira.issue(issue_key)
    print('{}: {}: {}:{}: {}'.format(singleIssue.key, singleIssue.fields.issuetype,
                                     singleIssue.fields.summary,
                                     singleIssue.fields.reporter.displayName, singleIssue.fields.issuelinks))
