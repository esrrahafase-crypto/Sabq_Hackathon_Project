import os
from dotenv import load_dotenv

load_dotenv()

# Elm / Nuha API settings
ELM_API_URL = os.getenv("ELM_API_URL")
ELM_API_KEY = os.getenv("ELM_API_KEY")
ELM_MODEL   = os.getenv("ELM_MODEL")

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
