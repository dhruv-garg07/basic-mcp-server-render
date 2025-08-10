# Basic MCP Server (FastAPI)

A tiny MCP server with **validate**, **ping**, and **echo** tools — made for quick Puch AI hackathon submission.

## Endpoints
- `GET /mcp` — Manifest (name, version, tools)
- `POST /mcp/validate` — Returns your phone in E.164 digits-only format if token is valid
- `POST /mcp/run` — Executes a tool (`ping`, `echo`)

## Env Vars
- `AUTH_TOKEN`  (required)  — your secret bearer token (aka *devtoken*)
- `PHONE_E164`  (required)  — your phone like `919876543210` (digits only)
- `PORT`        (Render/Heroku) — provided by host

## Quick Start (Local)
```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

export AUTH_TOKEN=changeme
export PHONE_E164=919000000000

uvicorn app.main:app --reload
```

## Deploy (Render)
1. Create a **Web Service** from this repo/zip.
2. Runtime: Python 3.11+
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Env Vars:
   - `AUTH_TOKEN=your-super-secret`
   - `PHONE_E164=919xxxxxxxxx` (digits only)
5. Open the URL: `https://<your-app>.onrender.com` (should show "ok")

## Connect from WhatsApp (Puch)
In your Puch hackathon chat, send:
```
/mcp connect https://<your-app>.onrender.com/mcp your-super-secret
```
On success you'll receive a share link like `https://puch.ai/mcp/<server_id>` — submit the `<server_id>`.

## Test Endpoints
```bash
# Manifest
curl https://<your-app>.onrender.com/mcp

# Validate (token in header)
curl -X POST https://<your-app>.onrender.com/mcp/validate          -H "Authorization: Bearer your-super-secret" -d '{}'

# Run ping
curl -X POST https://<your-app>.onrender.com/mcp/run          -H "Authorization: Bearer your-super-secret"          -H "Content-Type: application/json"          -d '{"tool":"ping","args":{}}'

# Run echo
curl -X POST https://<your-app>.onrender.com/mcp/run          -H "Authorization: Bearer your-super-secret"          -H "Content-Type: application/json"          -d '{"tool":"echo","args":{"text":"hello"}}'
```

---

## Render Blueprint (One-time setup)
1. Push this project to GitHub (or upload).
2. On Render: **New → Blueprint** and select your repo.
3. Review `render.yaml`. After deploy:
   - Render auto-generates `AUTH_TOKEN` (you can override in Dashboard).
   - Set `PHONE_E164` to your digits-only phone (e.g., `919876543210`).

## If creating a Web Service (not Blueprint)
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add Environment Variables:
  - `AUTH_TOKEN` = your secret
  - `PHONE_E164` = e.g., `919876543210`

## WhatsApp connect (Puch)
```
/mcp connect https://<your-app>.onrender.com/mcp <AUTH_TOKEN>
```
On success you’ll receive a share link like `https://puch.ai/mcp/<server_id>`.
