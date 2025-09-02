import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
import re
from collections import Counter

# 🚨 CSV File Path
csv_filename = "/Users/shiva/Desktop/Research Project/Bin1Organizations.csv"

print(f"📂 Checking if file exists: {csv_filename}")
if not os.path.exists(csv_filename):
    raise FileNotFoundError(f"🚨 File not found: {csv_filename}. Check the path.")

print("✅ File found. Loading CSV...")

# ✅ Load data with error handling & force all columns to be read as strings
try:
    df = pd.read_csv(csv_filename, dtype=str, low_memory=True)
    print(f"✅ CSV loaded successfully. {df.shape[0]} rows, {df.shape[1]} columns.")
except Exception as e:
    raise RuntimeError(f"❌ Error loading CSV file: {e}")

# 🚨 Column that contains the comments
preprocessed_column = "Comment"

if preprocessed_column not in df.columns:
    raise KeyError(f"🚨 Column '{preprocessed_column}' not found in CSV.")
print(f"✅ Column '{preprocessed_column}' found.")

# ✅ Fill NaN values with empty strings
df[preprocessed_column] = df[preprocessed_column].fillna("")

# 🚨 **STOP AT 400 COMMENTS**
df = df.head(400)
print(f"⚡ Processing only the first {df.shape[0]} comments.")

print("🔍 Converting comments to TF-IDF vectors...")
vectorizer = TfidfVectorizer(max_features=5000)
tfidf_matrix = vectorizer.fit_transform(df[preprocessed_column])
print(f"✅ TF-IDF conversion complete. Matrix shape: {tfidf_matrix.shape}")

# 🚨 Set similarity threshold
threshold = 0.6  

# ✅ Function to compute cosine similarity in chunks
def compute_similarity_chunked(tfidf_matrix, chunk_size=500):
    num_samples = tfidf_matrix.shape[0]
    similarity_matrix = np.zeros((num_samples, num_samples))

    print(f"⚡ Computing cosine similarity in chunks of {chunk_size}...")
    for start in range(0, num_samples, chunk_size):
        end = min(start + chunk_size, num_samples)
        similarity_matrix[start:end] = cosine_distances(tfidf_matrix[start:end], tfidf_matrix)
    print("✅ Cosine similarity computation complete.")

    return similarity_matrix

similarity_matrix = compute_similarity_chunked(tfidf_matrix)

print("🔍 Grouping similar comments...")
groups = []
visited = set()

for i in range(len(df)):
    if i in visited:
        continue
    group = [i]
    for j in range(i + 1, len(df)):
        if similarity_matrix[i, j] < (1 - threshold):
            group.append(j)
            visited.add(j)
    visited.add(i)
    groups.append(group)

print(f"✅ Grouping complete. Total groups formed: {len(groups)}")

# ✅ Assign group numbers
df["Group"] = -1
for group_id, group in enumerate(groups):
    for index in group:
        df.loc[index, "Group"] = group_id

# 🚨 Merge groups if there are too many
max_groups = 30
if len(groups) > max_groups:
    print(f"⚠️ Too many groups ({len(groups)}), merging to {max_groups}...")
    df["Merged_Group"] = pd.qcut(df["Group"].rank(method="first"), q=max_groups, labels=False)
else:
    df["Merged_Group"] = df["Group"]

# 🚨 Create output folder if it doesn't exist
output_folder = "/Users/shiva/Desktop/Research Project/Sorted_Comments2"
os.makedirs(output_folder, exist_ok=True)

# ✅ Save each group as a separate CSV file
group_summary = []

for group_id in sorted(df["Merged_Group"].unique()):
    group_df = df[df["Merged_Group"] == group_id]
    
    if len(group_df) < 5:
        continue  # Skip small groups

    group_filename = os.path.join(output_folder, f"Group_{group_id}.csv")
    group_df.to_csv(group_filename, index=False)

    print(f"📁 Saved Group {group_id}: {len(group_df)} comments → {group_filename}")
    group_summary.append({"Group": group_id, "File": group_filename, "Count": len(group_df)})

# ✅ Save group summary
summary_df = pd.DataFrame(group_summary)
summary_df.to_csv(os.path.join(output_folder, "Group_Summary.csv"), index=False)

print(f"✅ All groups saved! 📂 Check: {output_folder}")
