from datetime import datetime, timezone
import requests
from typing import List, Dict

def list_tools() -> List:
    return [
        {"name": "get_time", "description": "Returns actual time"},
        {"name": "fetch_url", "description": "Get data from provided url"}
    ]

def get_time() -> Dict[str, str]:
    return {
        "time": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    }

def fetch_url(url: str) -> Dict[str, str]:
    r = requests.get(url, timeout=5)
    return {
        "status": r.status_code,
        "content": r.text[:200]
    }


