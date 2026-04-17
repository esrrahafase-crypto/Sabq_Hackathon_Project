import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from config import TOP_K


def find_top_similar(user_idea: str, model, dataset: list, embeddings, top_k: int = TOP_K) -> list:
    """
    Convert user idea to embedding, compare with dataset,
    and return the top_k most similar ideas.
    """
    user_embedding = model.encode([user_idea])
    scores = cosine_similarity(user_embedding, embeddings)[0]

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "id": dataset[idx]["id"],
            "title": dataset[idx]["title"],
            "description": dataset[idx]["description"],
            "score": float(scores[idx])
        })

    return results
