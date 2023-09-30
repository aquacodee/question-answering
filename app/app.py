from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Initialize Elasticsearch connection
es = Elasticsearch(
    cloud_id="01b63b48f9e740d4824f7eaf3fe59119:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDAyMDg1MTJjMDE4YzQ2NjQ5YTQ2Y2Q2YzkxN2E4ZDEwJGY3YzUyNGM4MTdhODRjZjlhMjE2YTJjNDgwYzAxY2Ix"
)


@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        data = request.get_json()
        user_query = data["question"]

        # Implement logic to query Elasticsearch for relevant passages based on the user's question
        search_results = es.search(
            index="question_answering",  # Use the correct index name
            body={
                "query": {
                    "match": {
                        "passage": user_query  # Match the user's question with the passage content
                    }
                }
            },
            size=3,  # Number of passages to retrieve
        )

        # Process and format the search results
        answers = []
        for hit in search_results["hits"]["hits"]:
            passage = hit["_source"]["passage"]
            metadata = hit["_source"]["metadata"]
            answers.append({"passage": passage, "metadata": metadata})

        # Return the answers as a JSON response
        return jsonify({"answers": answers})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/upload", methods=["POST"])
def upload_document():
    try:
        data = request.get_json()

        # Extract document content and metadata from the request data
        document_content = data["content"]
        metadata = data["metadata"]

        # Create a new document with content and metadata
        new_document = {
            "passage": document_content,
            "metadata": metadata,
        }

        # Index the new document in Elasticsearch
        es.index(index="question_answering", body=new_document)

        # Optionally, you can refresh the index to make the new document searchable immediately
        es.indices.refresh(index="question_answering")

        # Return a success message as a JSON response
        return jsonify({"message": "Document uploaded and indexed successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
