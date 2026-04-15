import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "jira_issues.json")
vector_path = os.path.join(BASE_DIR, "vectordb", "jira_index.faiss")

# Ensure folder exists
os.makedirs(os.path.join(BASE_DIR, "vectordb"), exist_ok=True)

# Load data
with open(data_path, "r", encoding="utf-8") as f:
    issues = json.load(f)

# Prepare text
# texts = [i["summary"] + " " + str(i.get("description", "")) for i in issues]


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




if len(texts) == 0:
    raise ValueError("No data found in jira_issues.json")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
vectors = model.encode(texts)

print("Vectors shape:", vectors.shape)

# Create FAISS index
dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(vectors, dtype=np.float32))

# Save index
faiss.write_index(index, vector_path)

def search(query, k= len(texts)):
    """
    Search similar Jira issues using FAISS
    """

    # Convert query to embedding
    query_vector = model.encode([query])

    # Search FAISS
    D, I = index.search(np.array(query_vector, dtype=np.float32), k=k)

    results = []

    for i in I[0]:
        if i < len(issues):  # safety check
            results.append(issues[i])

    return results






# import os
# import json
# import numpy as np
# import faiss
# from sentence_transformers import SentenceTransformer

# # -------------------------------
# # 📁 Paths
# # -------------------------------
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# data_path = os.path.join(BASE_DIR, "data", "jira_issues.json")
# vector_path = os.path.join(BASE_DIR, "vectordb", "jira_index.faiss")

# os.makedirs(os.path.join(BASE_DIR, "vectordb"), exist_ok=True)

# # -------------------------------
# # 📥 Load data
# # -------------------------------
# with open(data_path, "r", encoding="utf-8") as f:
#     issues = json.load(f)

# # -------------------------------
# # 🧹 Clean text helpers
# # -------------------------------
# def clean_text(text):
#     if not text:
#         return ""
#     text = str(text)
#     text = text.replace("\n", " ").replace("\r", " ")
#     return text.strip()


# def clean_comments(comments):
#     """
#     Fix: comments causing bad embeddings
#     """
#     if not comments:
#         return ""

#     # Remove empty / duplicate / too long comments
#     cleaned = []
#     seen = set()

#     for c in comments:
#         c = clean_text(c)

#         if not c:
#             continue

#         if c in seen:
#             continue

#         # limit each comment length
#         c = c[:300]

#         seen.add(c)
#         cleaned.append(c)

#     # limit total comments (VERY IMPORTANT)
#     return " ".join(cleaned[:20])   # keep only top 5 comments


# # -------------------------------
# # 🧠 Prepare text
# # -------------------------------
# texts = []

# for issue in issues:
#     summary = clean_text(issue.get("summary", ""))
#     description = clean_text(issue.get("description", ""))

#     status = clean_text(issue.get("status", ""))
#     assignee = clean_text(issue.get("assignee", ""))
#     reporter = clean_text(issue.get("reporter", ""))
#     priority = clean_text(issue.get("priority", ""))
#     issuetype = clean_text(issue.get("issuetype", ""))
#     project = clean_text(issue.get("project", ""))

#     components = ", ".join(issue.get("components", []))
#     labels = ", ".join(issue.get("labels", []))
#     fix_versions = ", ".join(issue.get("fixVersions", []))
#     duedate = clean_text(issue.get("duedate", ""))

#     # 🔥 FIXED COMMENTS
#     comments = clean_comments(issue.get("comments", []))

#     # 🔥 Better structured text (important for embedding quality)
#     text = f"""
#     Issue {issue.get("key", "")}
#     Project: {project}
#     Type: {issuetype}
#     Summary: {summary}
#     Description: {description}
#     Status: {status}
#     Priority: {priority}
#     Assignee: {assignee}
#     Reporter: {reporter}
#     Components: {components}
#     Labels: {labels}
#     Fix Versions: {fix_versions}
#     Due Date: {duedate}
#     Comments: {comments}
#     """

#     texts.append(text.strip())


# if len(texts) == 0:
#     raise ValueError("No data found in jira_issues.json")

# # -------------------------------
# # 🤖 Load model
# # -------------------------------
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # -------------------------------
# # 🔢 Create embeddings
# # -------------------------------
# vectors = model.encode(texts, normalize_embeddings=True)

# print("Vectors shape:", vectors.shape)

# # -------------------------------
# # ⚡ FAISS (Cosine similarity)
# # -------------------------------
# dimension = vectors.shape[1]

# # 🔥 Use Inner Product (cosine similarity)
# index = faiss.IndexFlatIP(dimension)

# index.add(np.array(vectors, dtype=np.float32))

# # Save index
# faiss.write_index(index, vector_path)


# # -------------------------------
# # 🔍 Search
# # -------------------------------
# def search(query, k=len(texts)):
#     """
#     Search similar Jira issues using FAISS (cosine similarity)
#     """

#     query_vector = model.encode([query], normalize_embeddings=True)

#     D, I = index.search(np.array(query_vector, dtype=np.float32), k=len(texts))

#     results = []

#     for idx, score in zip(I[0], D[0]):
#         if idx < len(issues):
#             issue = issues[idx]
#             issue["score"] = float(score)  # similarity score
#             results.append(issue)

#     return results