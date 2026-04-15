import pandas as pd
import ast

'''Dataset Cleaner for creating the Knowledge Graph'''

# Load dataset
df = pd.read_csv("movies.csv")

# Helper to extract names from JSON-like columns
def extract_names(text):
    try:
        data = ast.literal_eval(text)
        return [item['name'] for item in data]
    except:
        return []

# Apply extraction
df['genres'] = df['genres'].apply(extract_names)
df['cast'] = df['cast'].apply(extract_names)
df['keywords'] = df['keywords'].apply(extract_names)
df['production_companies'] = df['production_companies'].apply(extract_names)

# Runtime bucket
def runtime_bucket(x):
    try:
        x = float(x)
        if x < 90:
            return "Short"
        elif x < 120:
            return "Medium"
        else:
            return "Long"
    except:
        return "Unknown"

df["runtime_bucket"] = df["runtime"].apply(runtime_bucket)

# Keep only required columns
df = df[[
    "title", "genres", "cast", "keywords",
    "production_companies", "director", "runtime_bucket"
]]

# Save cleaned file
df.to_csv("clean_movies.csv", index=False)

print("✅ Preprocessing done. Saved as clean_movies.csv")