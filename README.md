# 💡 Idea Originality Checker

An AI-powered Arabic web application that checks the originality of innovative ideas by comparing them against a database of existing patents/ideas, powered by Nuha (Elm's Arabic LLM).

---

## System Pipeline

1. **Input** — User types their idea in Arabic
2. **Embedding + Similarity** — The idea is converted to a vector embedding and compared against stored idea embeddings using cosine similarity
3. **Top 3 Retrieved** — The three most similar ideas are retrieved from the dataset
4. **LLM Analysis (Nuha)** — The user's idea + top 3 similar ideas are sent to Nuha, which returns a structured Arabic analysis
5. **Output** — The app displays similarity score, similar ideas, and detailed analysis
6. **Digital Fingerprint** *(optional)* — If the user wants to register their idea, a SHA-256 hash + timestamp record is saved locally

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| sentence-transformers | Arabic-capable text embeddings |
| scikit-learn | Cosine similarity calculation |
| Nuha (Elm LLM) | Arabic idea analysis via REST API |
| python-dotenv | Environment variable management |

---

## Project Structure

```
project/
├── .env                    # API credentials (do NOT commit to GitHub)
├── config.py               # All configuration constants
├── app.py                  # Main Streamlit UI
├── llm.py                  # Nuha API integration
├── embedder.py             # Embedding generation & caching
├── similarity.py           # Cosine similarity search
├── fingerprint.py          # Digital fingerprint logic
├── patentsDataset.json     # Ideas database
├── embeddings_cache.pkl    # Auto-generated embedding cache
├── submissions.json        # Auto-generated fingerprint records
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Setup Instructions

### 1. Clone or download the project
Clone the repository or download the project files to your local machine.

### 2. Create your `.env` file (do NOT commit it)
Create a `.env` file in the root directory and add your API credentials.

### 3. Example environment file

Use `.env.example` as a reference:
This file is only an example. Replace the values with your actual API credentials.

```
ELM_API_URL=your_api_url_here
ELM_API_KEY=your_api_key_here
ELM_MODEL=nuha-2.0
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Add the dataset
Make sure `patentsDataset.json` is placed in the root directory of the project before running the app.

---

## How to Run

```bash
streamlit run app.py
```

Then open your browser at: [http://localhost:8501](http://localhost:8501)

> **Note:** The first run will generate and cache embeddings automatically. Subsequent runs will load from cache and start faster.

---

## Notes

- The `.env` file must **never** be pushed to GitHub
- `embeddings_cache.pkl` is auto-generated on first run
- `submissions.json` stores all registered idea fingerprints locally
- Duplicate ideas (same hash) will not be saved again
- Ideas with similarity ≥ 85% cannot be fingerprinted
- - A `.gitignore` file is used to prevent sensitive files (like `.env`) from being uploaded to GitHub
