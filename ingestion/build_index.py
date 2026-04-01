

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
texts = [i["summary"] + " " + str(i.get("description", "")) for i in issues]

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

print("✅ FAISS index created at:", vector_path)