from jira import JIRA
import json
import os
from dotenv import load_dotenv
from jira.exceptions import JIRAError

load_dotenv(dotenv_path="../.env")  # go up one folder


email = os.getenv("email")
api_token = os.getenv("JIRA_API_TOKEN")
server =  os.getenv("server")


jira = JIRA(server=server, basic_auth=(email, api_token))
issues = jira.search_issues("project = 'AI_Hackathon'", maxResults=100)
# print("Total issues fetched:", len(issues))

# try:
#     jira = JIRA(server=server, basic_auth=(email, api_token))
#     jira.myself()
#     print("status = 200")
# except JIRAError as e:
#     code = e.status_code if e.status_code is not None else "unknown"
#     print(f"error: HTTP {code}")
#     if e.text:
#         print(e.text.strip())
#     raise SystemExit(1)
# except Exception as e:
#     print(f"error: {e}")
#     raise SystemExit(1)

data = []

# for issue in issues:
#     item = {
#         "id": issue.key,
#         "summary": issue.fields.summary,
#         "description": issue.fields.description
#     }
#     data.append(item)

for issue in issues:
    fields = issue.fields

    # Safe extraction helpers
    def safe_str(value):
        return str(value) if value else None

    def safe_name(value):
        return value.name if value else None

    def safe_list(values):
        return [v.name for v in values] if values else []

    def safe_comments(comments):
        return [c.body for c in comments.comments] if comments else []

    item = {
        "key": issue.key,
        "summary": fields.summary,
        "description": safe_str(fields.description),

        "status": safe_name(fields.status),
        "assignee": safe_str(fields.assignee),
        "reporter": safe_str(fields.reporter),
        "priority": safe_name(fields.priority),

        "created": fields.created,
        "updated": fields.updated,

        "issuetype": safe_name(fields.issuetype),
        "project": safe_name(fields.project),

        "components": safe_list(fields.components),
        "labels": fields.labels if fields.labels else [],

        "comments": safe_comments(fields.comment),

        "fixVersions": safe_list(fields.fixVersions),
        "duedate": fields.duedate if fields.duedate else None,
    }

    data.append(item)



# with open("../data/jira_issues.json", "w") as f:
#     json.dump(data, f, indent=4)

BASE_DIR = os.getcwd()
file_path = os.path.join(BASE_DIR, "data", "jira_issues.json")

with open(file_path, "w") as f:
    json.dump(data, f, indent=4)

print("Jira data saved")
# print(data)