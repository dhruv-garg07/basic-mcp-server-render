import os
from typing import Optional, Dict, Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "devtoken")
PHONE_E164 = os.getenv("PHONE_E164", "919000000000")  # digits only

app = FastAPI(title="Basic MCP Server", version="1.0.0")

@app.get("/")
def root():
    return {"ok": True, "service": "basic-mcp", "version": "1.0.0"}

@app.get("/mcp")
def manifest():
    return {
        "name": "basic-mcp",
        "version": "1.0.0",
        "tools": [
            {
                "name": "ping",
                "description": "Health check tool that returns 'pong'.",
                "input_schema": {"type": "object", "properties": {}}
            },
            {
                "name": "echo",
                "description": "Echo back the provided text.",
                "input_schema": {
                    "type": "object",
                    "properties": {"text": {"type": "string"}},
                    "required": ["text"]
                }
            },
        ],
    }

class ValidateRequest(BaseModel):
    token: Optional[str] = None

def _check_token(authorization: Optional[str], token_in_body: Optional[str]) -> None:
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
    elif token_in_body:
        token = token_in_body

    if token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/mcp/validate")
def validate(req: ValidateRequest, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    _check_token(authorization, req.token)
    # Puch expects digits-only phone to confirm ownership
    if not PHONE_E164.isdigit():
        raise HTTPException(status_code=400, detail="PHONE_E164 must be digits only, like 919876543210")
    return {"ok": True, "phone": PHONE_E164}

class RunRequest(BaseModel):
    tool: str
    args: Dict[str, Any] = {}

@app.post("/mcp/run")
def run_tool(req: RunRequest, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    _check_token(authorization, None)

    if req.tool == "ping":
        return {"ok": True, "result": "pong"}

    if req.tool == "echo":
        text = str(req.args.get("text", ""))
        return {"ok": True, "result": text}

    raise HTTPException(status_code=404, detail=f"Unknown tool: {req.tool}")