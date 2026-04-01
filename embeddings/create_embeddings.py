from sentence_transformers import SentenceTransformer
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/jira_issues.json") as f:
    issues = json.load(f)

# texts = []

# # for issue in issues:
# #     text = issue["summary"] + " " + str(issue["description"])
# #     texts.append(text)

# for issue in issues:
#     text = issue["summary"] + " " + str(issue["description"]) + " " + str(issue["comments"]) 
#     texts.append(text)


# embeddings = model.encode(texts)

# print("Embeddings created:", len(embeddings))
# # print(embeddings)


texts = []

for issue in issues:
    # Safe extraction
    summary = issue.get("summary", "")
    description = str(issue.get("description", ""))
    status = issue.get("status", "")
    assignee = issue.get("assignee", "")
    reporter = issue.get("reporter", "")
    priority = issue.get("priority", "")
    issuetype = issue.get("issuetype", "")
    project = issue.get("project", "")
    components = ", ".join(issue.get("components", []))
    labels = ", ".join(issue.get("labels", []))
    comments = " ".join(issue.get("comments", []))
    fix_versions = ", ".join(issue.get("fixVersions", []))
    duedate = str(issue.get("duedate", ""))

    # 🔥 Build rich context text
    text = f"""
    Issue ID: {issue.get("key", "")}
    Project: {project}
    Type: {issuetype}
    Summary: {summary}
    Description: {description}
    Status: {status}
    Priority: {priority}
    Assignee: {assignee}
    Reporter: {reporter}
    Components: {components}
    Labels: {labels}
    Fix Versions: {fix_versions}
    Due Date: {duedate}
    Comments: {comments}
    """

    texts.append(text.strip())

# Generate embeddings
embeddings = model.encode(texts, show_progress_bar=True)

print("✅ Embeddings created:", len(embeddings))