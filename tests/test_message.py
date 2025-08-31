def test_message_requires_auth(client):
    # no header auth -> 401
    resp = client.post("/message?session_id=abc123", json={})
    assert resp.status_code in (401, 403)

def test_message_missing_session_id(client, auth_headers):
    resp = client.post("/message", headers=auth_headers, json={})
    assert resp.status_code == 422

def test_message_invalid_body(client, auth_headers):
    resp = client.post("/message?session_id=abc123", headers=auth_headers, json={})
    assert resp.status_code == 422

def test_message_list_tools_queues(client, auth_headers):
    payload = {
        "type": "list_tools",
        "request_id": "req-1",
        "data": {}
    }
    resp = client.post("/message?session_id=abc123", headers=auth_headers, json=payload)
    assert resp.status_code == 200
    data = resp.json()

    assert isinstance(data, dict)
    assert data.get("status") in ("queued", "ok", "accepted")