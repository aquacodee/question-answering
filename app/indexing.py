from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Initialize Elasticsearch client
es = Elasticsearch(["https://elasticsearch:9200"], verify_certs=False)

# Initialize SentenceTransformers model
model = SentenceTransformer("all-mpnet-base-v2")

# Load user queries
user_queries = [
    "Which story is this?",
    "is the story interesting?",
    "What is the of the story?",
    # Add more questions as needed
]

# Create a DataFrame to store the results
results_data = {
    "Question": [],
    "Passage 1": [],
    "Relevance Score 1": [],
    "Passage 1 Metadata": [],
    "Passage 2": [],
    "Relevance Score 2": [],
    "Passage 2 Metadata": [],
    "Passage 3": [],
    "Relevance Score 3": [],
    "Passage 3 Metadata": [],
}

# Define the Elasticsearch index name
index_name = "passage_index"

# Process each user query and retrieve relevant passages
for query in user_queries:
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Elasticsearch search query to find similar passages
    search_query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'Embedding') + 1.0",
                    "params": {"query_vector": query_embedding.tolist()},
                },
            }
        },
        "size": 3,  # Retrieve the top 3 passages
        "_source": ["Passage", "Metadata", "Embedding"],
    }

    # Perform the search
    search_results = es.search(index=index_name, body=search_query)

    # Extract relevant passages and metadata
    passages = []
    metadata = []
    relevance_scores = []

    for hit in search_results["hits"]["hits"]:
        passages.append(hit["_source"]["Passage"])
        metadata.append(hit["_source"]["Metadata"])
        relevance_scores.append(hit["_score"])

    # Add the results to the DataFrame
    results_data["Question"].append(query)
    for i in range(3):
        results_data[f"Passage {i+1}"].append(passages[i])
        results_data[f"Relevance Score {i+1}"].append(relevance_scores[i])
        results_data[f"Passage {i+1} Metadata"].append(metadata[i])

# Create a DataFrame from the results
results_df = pd.DataFrame(results_data)

# Save the results to a CSV file
results_df.to_csv("questions_answers.csv", index=False)
