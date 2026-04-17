import os
import json
import pickle
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, CACHE_FILE, DATASET_FILE


def load_dataset():
    # Load patents dataset from JSON file
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_combined_text(item):
    # Combine title and description for embedding
    return item["title"] + " " + item["description"]


def load_or_generate_embeddings():
    """
    Load embeddings from cache if available, otherwise generate and cache them.
    """
    model = SentenceTransformer(EMBEDDING_MODEL)
    dataset = load_dataset()

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
        return model, dataset, cache["embeddings"]

    texts = [get_combined_text(item) for item in dataset]
    embeddings = model.encode(texts, show_progress_bar=True)

    with open(CACHE_FILE, "wb") as f:
        pickle.dump({"embeddings": embeddings}, f)

    return model, dataset, embeddings
