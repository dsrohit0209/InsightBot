from jira import JIRA
import json
import os
from dotenv import load_dotenv
from jira.exceptions import JIRAError

load_dotenv(dotenv_path="../.env")  # go up one folder

email = "dsrohit0209@gmail.com"
api_token = os.getenv("JIRA_API_TOKEN")
server = "https://dsrohit0209.atlassian.net/"

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


jira = JIRA(server=server, basic_auth=(email, api_token))
issues = jira.search_issues("project IN ('SCRUM','LI')", maxResults=1000)
# print("Total issues fetched:", len(issues))

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

# for issue in issues:
#     issue_data = {}

#     # Access all raw fields dynamically
#     fields = issue.raw["fields"]

#     for key, value in fields.items():
#         issue_data[key] = value

#     data.append(issue_data)    

# with open("../data/jira_issues.json", "w") as f:
#     json.dump(data, f, indent=4)

BASE_DIR = os.getcwd()
file_path = os.path.join(BASE_DIR, "data", "jira_issues.json")

with open(file_path, "w") as f:
    json.dump(data, f, indent=4)

print("Jira data saved")
print(len(data))













# from jira import JIRA
# import json
# import os
# from dotenv import load_dotenv
# from jira.exceptions import JIRAError

# load_dotenv(dotenv_path="../.env")  # go up one folder


# EMAIL = os.getenv("email")
# API_TOKEN = os.getenv("JIRA_API_TOKEN")
# JIRA_URL = os.getenv("server")


# jira = JIRA(
#     server=JIRA_URL,
#     basic_auth=(EMAIL, API_TOKEN)
# )

# # -------------------------------
# # 📌 Projects you want to fetch
# # -------------------------------
# PROJECT_KEYS = ["AI_Hackathon", "LLM improvement", "Support"]  # Add multiple projects here

# # -------------------------------
# # 📥 Fetch issues function
# # -------------------------------
# def fetch_issues(project_key):
#     issues_data = []
#     start_at = 0
#     max_results = 500

#     while True:
#         issues = jira.enhanced_search_issues(
#             f'project = "{project_key}" ORDER BY created DESC',
#             maxResults=max_results,
#             fields="summary,status,assignee,description,reporter,priority,created,updated,issuetype,project,components," \
#             "labels,comment,fixVersions,duedate"
#         )

#         if not issues:
#             break

#         data = []

#         for issue in issues:
#             fields = issue.fields

#             # Safe extraction helpers
#             def safe_str(value):
#                 return str(value) if value else None

#             def safe_name(value):
#                 return value.name if value else None

#             def safe_list(values):
#                 return [v.name for v in values] if values else []

#             def safe_comments(comments):
#                 return [c.body for c in comments.comments] if comments else []

#             item = {
#                 "key": issue.key,
#                 "summary": fields.summary,
#                 "description": safe_str(fields.description),

#                 "status": safe_name(fields.status),
#                 "assignee": safe_str(fields.assignee),
#                 "reporter": safe_str(fields.reporter),
#                 "priority": safe_name(fields.priority),

#                 "created": fields.created,
#                 "updated": fields.updated,

#                 "issuetype": safe_name(fields.issuetype),
#                 "project": safe_name(fields.project),

#                 "components": safe_list(fields.components),
#                 "labels": fields.labels if fields.labels else [],

#                 "comments": safe_comments(fields.comment),

#                 "fixVersions": safe_list(fields.fixVersions),
#                 "duedate": fields.duedate if fields.duedate else None,
#             }
#             issues_data.append(item)


#         start_at += max_results

#         # Break if fewer issues returned than max_results (no more pages)
#         if len(issues) < max_results:
#             break

#     return issues_data

# # -------------------------------
# # 🔄 Fetch all projects
# # -------------------------------
# all_issues = []

# for project in PROJECT_KEYS:
#     print(f"Fetching issues for {project}...")
#     project_issues = fetch_issues(project)
#     all_issues.extend(project_issues)

# print(f"\n✅ Total issues fetched: {len(all_issues)}")

# # -------------------------------
# # 💾 Save to CSV
# # -------------------------------
# # df = pd.DataFrame(all_issues)
# # df.to_csv("jira_issues.csv", index=False)
# # print("✅ Saved to jira_issues.csv")

# BASE_DIR = os.getcwd()
# file_path = os.path.join(BASE_DIR, "data", "jira_issues.json")

# with open(file_path, "w") as f:
#     json.dump(all_issues, f, indent=4)

# print("Jira data saved")
# # print(data)








# from jira import JIRA
# import json
# import os
# import time
# from dotenv import load_dotenv

# # -------------------------------
# # 🔐 Load environment variables
# # -------------------------------
# load_dotenv(dotenv_path="../.env")

# EMAIL = os.getenv("email")
# API_TOKEN = os.getenv("JIRA_API_TOKEN")
# JIRA_URL = os.getenv("server")

# # -------------------------------
# # 🔌 Jira connection (with timeout)
# # -------------------------------
# jira = JIRA(
#     server=JIRA_URL,
#     basic_auth=(EMAIL, API_TOKEN),
#     timeout=30
# )

# # -------------------------------
# # 📌 Projects
# # -------------------------------
# PROJECT_KEYS = ["AI_Hackathon", "LLM improvement", "Support"]

# # -------------------------------
# # 🛠 Helpers
# # -------------------------------
# def safe_convert(value):
#     """Convert any Jira field safely to string/list"""
#     try:
#         if value is None:
#             return None
#         if isinstance(value, list):
#             return [str(v) for v in value]
#         return str(value)
#     except:
#         return None


# def fetch_comments(issue_key):
#     """Fetch comments separately (safe)"""
#     try:
#         comments = jira.comments(issue_key)
#         return [c.body for c in comments]
#     except:
#         return []


# # -------------------------------
# # 📥 Fetch issues (core logic)
# # -------------------------------
# def fetch_issues(project_key):
#     issues_data = []
#     start_at = 0
#     max_results = 500   # 🔥 small batch prevents hanging
#     retry_count = 3

#     while True:
#         print(f"📥 Fetching {project_key}: {start_at} → {start_at + max_results}")

#         for attempt in range(retry_count):
#             try:
#                 issues = jira.enhanced_search_issues(
#                     f'project = "{project_key}" ORDER BY created DESC',
#                     startAt=start_at,      # ✅ CRITICAL FIX
#                     maxResults=max_results,
#                     fields="*all"
#                 )
#                 break
#             except Exception as e:
#                 print(f"⚠️ Retry {attempt+1}/{retry_count}:", e)
#                 time.sleep(3)
#         else:
#             print("❌ Skipping batch due to repeated failures")
#             break

#         if not issues:
#             break

#         for issue in issues:
#             try:
#                 fields = issue.fields
#                 item = {"key": issue.key}

#                 # ✅ Dynamically extract ALL fields
#                 for attr in dir(fields):
#                     if attr.startswith("_"):
#                         continue
#                     try:
#                         value = getattr(fields, attr)
#                         item[attr] = safe_convert(value)
#                     except:
#                         item[attr] = None

#                 # ✅ Fetch comments separately (avoids crash)
#                 item["comments"] = fetch_comments(issue.key)

#                 issues_data.append(item)

#             except Exception as e:
#                 print(f"⚠️ Skipping issue {issue.key}:", e)

#         start_at += max_results

#         # ✅ Exit when last page reached
#         if len(issues) < max_results:
#             break

#     return issues_data


# # -------------------------------
# # 🔄 Fetch all projects
# # -------------------------------
# all_issues = []

# for project in PROJECT_KEYS:
#     print(f"\n🚀 Starting project: {project}")
#     project_issues = fetch_issues(project)
#     all_issues.extend(project_issues)

# print(f"\n✅ Total issues fetched: {len(all_issues)}")


# # -------------------------------
# # 💾 Save JSON
# # -------------------------------
# BASE_DIR = os.getcwd()
# os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

# file_path = os.path.join(BASE_DIR, "data", "jira_issues.json")

# with open(file_path, "w", encoding="utf-8") as f:
#     json.dump(all_issues, f, indent=4, ensure_ascii=False)

# print("✅ Jira data saved successfully")








#######V3


# from jira import JIRA
# import json
# import os
# import time
# from dotenv import load_dotenv

# # -------------------------------
# # 🔐 Load env
# # -------------------------------
# load_dotenv(dotenv_path="../.env")

# EMAIL = os.getenv("email")
# API_TOKEN = os.getenv("JIRA_API_TOKEN")
# JIRA_URL = os.getenv("server")

# # -------------------------------
# # 🔌 Jira connection
# # -------------------------------
# jira = JIRA(
#     server=JIRA_URL,
#     basic_auth=(EMAIL, API_TOKEN),
#     timeout=30
# )

# # -------------------------------
# # 📌 Projects
# # -------------------------------
# PROJECT_KEYS = ["AI_Hackathon", "LLM improvement", "Support"]

# # -------------------------------
# # 🛠 Helpers
# # -------------------------------
# def safe_convert(value):
#     try:
#         if value is None:
#             return None
#         if isinstance(value, list):
#             return [str(v) for v in value]
#         return str(value)
#     except:
#         return None


# def fetch_comments(issue_key):
#     try:
#         comments = jira.comments(issue_key)
#         return [c.body for c in comments]
#     except:
#         return []


# # -------------------------------
# # 📥 Fetch issues (WORKING)
# # -------------------------------
# def fetch_issues(project_key):
#     issues_data = []
#     start_at = 0
#     max_results = 50  # safe batch size

#     while True:
#         print(f"📥 Fetching {project_key}: {start_at} → {start_at + max_results}")

#         try:
#             issues = jira.search_issues(
#                 f'project = "{project_key}" ORDER BY created DESC',
#                 startAt=start_at,
#                 maxResults=max_results,
#                 fields="*all"
#             )
#         except Exception as e:
#             print("⚠️ Error, retrying...", e)
#             time.sleep(3)
#             continue

#         if not issues:
#             break

#         for issue in issues:
#             try:
#                 fields = issue.fields
#                 item = {"key": issue.key}

#                 # ✅ extract all fields dynamically
#                 for attr in dir(fields):
#                     if attr.startswith("_"):
#                         continue
#                     try:
#                         value = getattr(fields, attr)
#                         item[attr] = safe_convert(value)
#                     except:
#                         item[attr] = None

#                 # ✅ fetch comments separately
#                 item["comments"] = fetch_comments(issue.key)

#                 issues_data.append(item)

#             except Exception as e:
#                 print(f"⚠️ Skipping issue {issue.key}:", e)

#         start_at += max_results

#         if len(issues) < max_results:
#             break

#     return issues_data


# # -------------------------------
# # 🔄 Run
# # -------------------------------
# all_issues = []

# for project in PROJECT_KEYS:
#     print(f"\n🚀 Starting project: {project}")
#     project_issues = fetch_issues(project)
#     all_issues.extend(project_issues)

# print(f"\n✅ Total issues fetched: {len(all_issues)}")

# # -------------------------------
# # 💾 Save
# # -------------------------------
# BASE_DIR = os.getcwd()
# os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

# file_path = os.path.join(BASE_DIR, "data", "jira_issues.json")

# with open(file_path, "w", encoding="utf-8") as f:
#     json.dump(all_issues, f, indent=4, ensure_ascii=False)

# print("✅ Jira data saved successfully")