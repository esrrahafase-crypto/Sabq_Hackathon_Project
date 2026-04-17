import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_secret(name: str):
    try:
        return st.secrets[name]
    except:
        return os.getenv(name)


# Elm / Nuha API settings
ELM_API_URL = get_secret("ELM_API_URL")
ELM_API_KEY = get_secret("ELM_API_KEY")
ELM_MODEL   = get_secret("ELM_MODEL")

# Embedding model
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# Search settings
TOP_K = 3

# Similarity threshold above which fingerprint is rejected
FINGERPRINT_REJECT_THRESHOLD = 0.85

# File paths
DATASET_FILE   = "patentsDataset.json"
CACHE_FILE     = "embeddings_cache.pkl"
RECORDS_FILE   = "submissions.json"
