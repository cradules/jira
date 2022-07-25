import re
from jira import JIRA

jira = JIRA("https://jira.sdlcpoc.eu")

projects = JIRA.project()
