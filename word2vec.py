import pandas as pd
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load comments from CSV
file_path = '/Users/shiva/Desktop/bin1_comments.csv'
comment_column = 'bin1_cleaned'  # Replace with the column name containing comments
df = pd.read_csv(file_path)

# Tokenize comments
comments = [comment.split() for comment in df[comment_column].dropna().tolist()]

#Parameters
word2vec_model = Word2Vec(
    sentences=comments,    
    vector_size=100,       
    window=3,              
    min_count=3,           
    workers=4,             
    sg=1                   
)

# example phrases for each bin
example_phrases = {
     "Funding and Financial Concerns": [
        "Medicare", "Medicaid", "payment transparency", 
        "financial accountability", "profit diversion", "fund allocation", 
        "public funds misuse"
    ],
    "Workforce and Staffing Challenges": [
        "nurse shortage", "understaffing", "staffing crisis", "workforce gaps", 
        "high workloads", "burnout", "hiring challenges", 
        "certified nursing assistants", "licensed practical nurses"
    ],
    "Personal Experiences and Caregiving Challenges": [
        "family caregiving", "personal care", "social worker challenges", 
        "caregiver workload", "resident care difficulties", "caregiver burnout"
    ],
    "Resident Experience and Quality of Care": [
        "resident rights", "resident well-being", "care quality standards", 
        "nursing home outcomes", "geriatric care improvements", 
        "resident satisfaction", "elder care reforms"
    ],
    "Policy Opposition and Implementation Concerns": [
        "policy challenges", "NPRM objections", "implementation hurdles", 
        "regulatory concerns", "policy reform opposition", "compliance issues", 
        "nursing home oversight"
    ]
}


# compute bin centroids using example phrases
def get_phrase_vector(phrases, model):
    vectors = []
    for phrase in phrases:
        tokens = phrase.split()  # Split phrases into words
        for token in tokens:
            if token in model.wv:
                vectors.append(model.wv[token])
    return np.mean(vectors, axis=0) if vectors else np.zeros(model.vector_size)

bin_vectors = {bin_name: get_phrase_vector(phrases, word2vec_model) 
               for bin_name, phrases in example_phrases.items()}

# Compute comment vectors
def get_comment_vector(comment_tokens, model):
    vectors = [model.wv[token] for token in comment_tokens if token in model.wv]
    return np.mean(vectors, axis=0) if vectors else np.zeros(model.vector_size)

comment_vectors = [get_comment_vector(comment, word2vec_model) for comment in comments]

# ssign comments to bins based on cosine similarity
def assign_to_bin(comment_vector, bin_vectors, threshold=0.2):
    similarities = {bin_name: cosine_similarity([comment_vector], [bin_vector])[0][0] 
                    for bin_name, bin_vector in bin_vectors.items()}
    max_bin = max(similarities, key=similarities.get)
    max_similarity = similarities[max_bin]
    return max_bin if max_similarity >= threshold else None  # Assign None if similarity is below the threshold

assignments = [assign_to_bin(comment_vector, bin_vectors) for comment_vector in comment_vectors]

# Add results to the original CSV
df['Assigned Bin'] = assignments

# Count comments in each bin
bin_counts = df['Assigned Bin'].value_counts()
neither_bin = df[df['Assigned Bin'].isnull()][comment_column].tolist()

# Print results
print("Bin Counts:")
print(bin_counts)

if neither_bin:
    print("\nComments in Neither Bin:")
    for comment in neither_bin:
        print(comment)

# Save the results to a new CSV file
output_file = 'comments_with_bins.csv'
df.to_csv(output_file, index=False)

print(f"\nResults saved to {output_file}")
