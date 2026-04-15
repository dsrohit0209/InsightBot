from jira import JIRA
import os

EMAIL = os.getenv("email")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = os.getenv("server")

jira = JIRA(
    server=JIRA_URL,
    basic_auth=(EMAIL, API_TOKEN)
)

def create_jira_ticket(summary, description, project_key="AI_Hackathon", issue_type="Task"):
    issue_dict = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
    }

    new_issue = jira.create_issue(fields=issue_dict)
    return new_issue.key