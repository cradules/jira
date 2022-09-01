import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from jira import JIRA
from misc import models, schemas
from misc.database import SessionLocal, engine
from misc.crud_r4j import create_items
from misc.database import get_db
import sqlite3
import os

HOST_URL = os.getenv('HOST_URL')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
PROJECT_ID = os.getenv('PROJECT_ID')

jira = JIRA(server=HOST_URL, basic_auth=(USER, PASSWORD))

data_dir = "sql_app.db"

con = sqlite3.connect(data_dir, check_same_thread=False)
cur = con.cursor()

app = FastAPI()


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


# Extract the ID filed by field name
def id_field(field_name):
    fields = jira.fields()

    for f in fields:
        if f['name'] == field_name:
            return f['id']


# Update DB "linked_issue" column
def update_issue_link():
    shrs = cur.execute("SELECT issue_id FROM items WHERE issue_type != 'Business Requirements'")
    for shr in shrs:
        issue_id = jira.issue(shr[0])
        issue_links = issue_id.fields.issuelinks
        for link in issue_links:
            if hasattr(link, "outwardIssue"):
                outwardIssue = link.outwardIssue
                outwardIssue_type = link.type.outward
                print(outwardIssue_type)
                print("\tOutward: " + outwardIssue.key)
                if 'part of requirement' in str(outwardIssue_type):
                    query = f"UPDATE items SET linked_issues = '{outwardIssue}' WHERE issue_id = '{issue_id}'"
                    print(query)
                    c = con.cursor()
                    c.execute(query)
                    c.fetchall()
        con.commit()


# Update
def update_br_specific_id(filed_name):
    cur.execute("SELECT issue_id FROM items WHERE issue_type = 'Business Requirements'")
    queries = cur.fetchall()
    for query in queries:
        cur.execute('SELECT package FROM items WHERE issue_id = ?', query)
        package_raw = cur.fetchall()
        package = package_raw[0][0]
        issue = jira.issue(query)
        field_id = id_field(filed_name)
        issue.update(fields={field_id: package})


models.Base.metadata.create_all(bind=engine)


# updatge SHR

# Does the requirement I'm trying to name a father in the same package?
#
# YES --> is there more than one father in the same package?
#
# ____YES--> take any (e.g. the lowest number one)
#
# ____NO--> Take that one
#
# NO--> put 00 in the position of the name that belongs to the father

@app.post("/items/")
def create_item_db(
        project_id: str,
        db: Session = Depends(get_db)

):
    create_items(db=db, project_id=project_id)
    update_issue_link()
    update_br_specific_id('RP Specific ID')
    return "Done"


uvicorn.run(app, host="0.0.0.0", port=5001, log_level="info")
