import hashlib
import json
import os
from datetime import datetime
from config import RECORDS_FILE, FINGERPRINT_REJECT_THRESHOLD


def generate_fingerprint(user_idea: str, top_score: float) -> dict:
    """
    Generate a digital fingerprint for the idea.
    Returns the record dict, or raises ValueError if rejected.
    """
    # Reject if similarity is too high
    if top_score >= FINGERPRINT_REJECT_THRESHOLD:
        raise ValueError("high_similarity")

    idea_hash = hashlib.sha256(user_idea.strip().encode("utf-8")).hexdigest()

    # Check for duplicate hash
    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            try:
                records = json.load(f)
                for r in records:
                    if r.get("hash") == idea_hash:
                        raise ValueError("duplicate")
            except json.JSONDecodeError:
                pass

    timestamp = datetime.now().isoformat()

    record = {
        "idea": user_idea,
        "hash": idea_hash,
        "timestamp": timestamp,
        "top_similarity_score": round(top_score, 4)
    }

    return record


def save_record(record: dict):
    """
    Append the record to the submissions JSON file.
    """
    records = []

    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            try:
                records = json.load(f)
            except json.JSONDecodeError:
                records = []

    records.append(record)

    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
