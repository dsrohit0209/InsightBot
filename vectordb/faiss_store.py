import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Get project root directory
BASE_DIR = os.getcwd()

DATA_PATH = os.path.join(BASE_DIR, "data", "jira_issues.json")
VECTOR_PATH = os.path.join(BASE_DIR, "vectordb", "jira_index.faiss")

# Make sure vectordb folder exists
os.makedirs(os.path.join(BASE_DIR, "vectordb"), exist_ok=True)

print("Loading JSON from:", DATA_PATH)
print("Saving FAISS to:", VECTOR_PATH)

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load Jira issues
with open(DATA_PATH, "r", encoding="utf-8") as f:
    issues = json.load(f)

# Prepare texts
texts = [i["summary"] + " " + str(i.get("description", "")) for i in issues]

if len(texts) == 0:
    raise ValueError("No texts found in jira_issues.json!")

# Create embeddings
vectors = model.encode(texts)

print("Vectors shape:", vectors.shape)

# Create FAISS index
dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(vectors, dtype=np.float32))

# Save index
faiss.write_index(index, VECTOR_PATH)

print(VECTOR_PATH)
print("✅ FAISS index created successfully!")
print("Saved at:", VECTOR_PATH)
