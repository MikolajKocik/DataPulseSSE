from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from queue import Queue
import json, asyncio
from app.models.mcp_response import MCPResponse
from app.models.mcp_request import MCPRequest
from app.models.error_response import ErrorResponse
from app.tools import list_tools, get_time, fetch_url
from app.auth import verify_bearer
from app.session import create_session, validate_session, cleanup_sessions

app = FastAPI()
queues = {}

@app.get("/events")
async def events(session_id: str, auth=Depends(verify_bearer)):
    if not validate_session(session_id):
        create_session(session_id)
    
    q: Queue = queues.setdefault(session_id, Queue())

    async def event_stream():
        while True:
            cleanup_sessions()
            try:
                msg = q.get(timeout=10)
                yield f"data: {json.dumps(msg)}\n\n"
            except:
                # Send an SSE comment as a heartbeat to keep the connection alive
                yield ": ping\n\n"
                # Small pause to avoid busy‑looping and reduce CPU usage
                await asyncio.sleep(0.1)
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )

@app.post("/message")
async def message(req: MCPRequest, session_id: str, auth=Depends(verify_bearer)):
    if not validate_session(session_id):
        return ErrorResponse(type="error", request_id=req.request_id, error="Invalid session")
   
    q = queues.setdefault(session_id, Queue())

    try:
        # return list tools
        if req.type == "list_tools":
            resp = MCPResponse(type="list_tools", request_id=req.request_id, data=list_tools())
        # return specific tool
        elif req.type == "call_tool":
            tool = req.data.get("name")
            if tool == "get_time":
                resp = MCPResponse(type="tool_result", request_id=req.request_id, data=get_time())
            elif tool == "fetch_url":
                resp = MCPResponse(type="tool_result", request_id=req.request_id, data=fetch_url(req.data["url"]))
            else:
                raise ValueError("Unknown tool")
        else:
            raise ValueError("Unknow request type")
    except Exception as e:
                resp = ErrorResponse(type="error", request_id=req.request_id, error=str(e))
    
    # convert model to dict
    q.put(resp.model_dump())

    return {"status": "queued"}