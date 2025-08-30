import time
from typing import Dict

SESSION_TTL = 3600 # 1h
_sessions: Dict[str, float] = {}

def create_session(session_id: str):
    _sessions[session_id] = time.time() + SESSION_TTL

def validate_session(session_id: str):
    exp = _sessions.get(session_id)
    if not exp or exp < time.time():
        _sessions.pop(session_id, None)
        return False
    return True

def cleanup_sessions():
    now = time.time()
    expired = [sid for sid, exp in _sessions.items() if exp < now]
    for sid in expired:
        _sessions.pop(sid, None)
