import json
import time

def _sse_data_lines(stream_response, timeout_sec=5):
    """Generator returns payloads data as dict"""
    deadline = time.time() + timeout_sec
    for line in stream_response.iter_lines():
        if isinstance(line, bytes):
            line = line.decode("utf-8", errors="ignore")

        if time.time() > deadline:
            break

        # skip keep-alive comments ": ping"
        if not line or line.startswith(":"):
            continue

        if line.startswith("data: "):
            payload = line[len("data: ") :]
            try: 
                yield json.loads(payload)
            except Exception:
                # if not json -> skip
                continue

def test_sse_roundtrip_list_tools(client, auth_headers):
    session_id = "sse-test-1"
    # open stream sse
    with client.stream("GET", f"/events?session_id={session_id}", headers=auth_headers) as r:
        assert r.status_code == 200

        payload = {
            "type": "list_tools",
            "request_id": "req-see-1",
            "data": {}
        }
        post_resp = client.post(f"/message?session_id={session_id}", headers=auth_headers, json=payload)

        # get although one event
        got = None
        for evt in _sse_data_lines(r, timeout_sec=5):
            # expect request_id 
            if isinstance(evt, dict) and evt.get("request_id") == "req-sse-1":
                got = evt
                break
        
        assert got is not None, "Expected SSE event not received"
        assert got.get("type") in ("list_tools", "tool_result")