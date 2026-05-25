"""
TerrificName AI — ElevenLabs Hack #10 Voice Domain Broker
Uses REAL ElevenLabs Speech Engine SDK v2.48+ API
"""
import os
import sys
import asyncio
import traceback
import json as _json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ── Load .env ─────────────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_OK = True
except Exception as e:
    DOTENV_OK = False

# ── Config ────────────────────────────────────────────────────────────────────
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
PORT = int(os.environ.get("PORT", 8000))
ENV = os.environ.get("ENV", "production")
SPEECH_ENGINE_PORT = int(os.environ.get("SPEECH_ENGINE_PORT", 3001))

CLAUDE_MODELS = [
    os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6"),
    "claude-sonnet-4-6",
    "claude-opus-4-6",
    "claude-haiku-4-5-20251001",
    "claude-3-5-sonnet-20241022",
]
CLAUDE_MODEL = CLAUDE_MODELS[0]

print("=" * 60)
print("TERRIFICNAME AI — STARTUP")
print("=" * 60)
print(f"dotenv: {DOTENV_OK}")
print(f"Anthropic key: {'SET' if ANTHROPIC_API_KEY else 'MISSING'}")
print(f"ElevenLabs key: {'SET' if ELEVENLABS_API_KEY else 'MISSING'}")
print(f"Claude model: {CLAUDE_MODEL}")
print(f"Ports: HTTP={PORT}, SpeechEngine={SPEECH_ENGINE_PORT}")

# ── Anthropic client ─────────────────────────────────────────────────────────
anthropic_client = None
try:
    import anthropic
    if ANTHROPIC_API_KEY:
        anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        print("✅ Anthropic client ready")
    else:
        print("⚠️  No ANTHROPIC_API_KEY")
except Exception as e:
    print(f"❌ Anthropic failed: {e}")

# ── Domain engine ────────────────────────────────────────────────────────────
DOMAIN_ENGINE_OK = False
DOMAINS = []
VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
SYSTEM_PROMPT = "You are TerrificName AI, a voice domain broker with 412 premium domains. Keep responses under 60 words, natural speech, no markdown."

try:
    from domain_engine import SYSTEM_PROMPT as DE_PROMPT, DOMAINS as DE_DOMAINS, search_domains
    SYSTEM_PROMPT = DE_PROMPT
    DOMAINS = DE_DOMAINS
    DOMAIN_ENGINE_OK = True
    print(f"✅ Domain engine: {len(DOMAINS)} domains")
except Exception as e:
    print(f"⚠️  Domain engine failed: {e}")
    traceback.print_exc()
    def search_domains(q, top_k=10): return []

# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(title="TerrificName AI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── REAL ElevenLabs Speech Engine (v2.48+ SDK) ────────────────────────────────
# Based on: https://github.com/elevenlabs/elevenlabs-python
# Speech Engine is async-only, available on AsyncElevenLabs
# engine = await elevenlabs.speech_engine.get("seng_123")
# await engine.serve(port=3001, on_transcript=..., on_init=..., on_close=...)
# ─────────────────────────────────────────────────────────────────────────────
SPEECH_ENGINE_RUNNING = False

async def start_speech_engine():
    """Start the ElevenLabs Speech Engine server in background."""
    global SPEECH_ENGINE_RUNNING

    if not ELEVENLABS_API_KEY:
        print("ℹ️  Skipping Speech Engine — no ELEVENLABS_API_KEY")
        return

    if not DOMAIN_ENGINE_OK:
        print("ℹ️  Skipping Speech Engine — domain engine failed")
        return

    try:
        from elevenlabs import AsyncElevenLabs
        import openai

        elevenlabs_async = AsyncElevenLabs(api_key=ELEVENLABS_API_KEY)

        # Get or create a speech engine
        # For Hackathon: we use a default engine or create one via API
        # The SDK uses engine IDs like "seng_123"
        # For demo purposes, we'll try to get a default engine
        print("🎙️  Initializing Speech Engine...")

        # Try to list available engines and use the first one
        # Or create a simple engine via the API
        # For the hackathon, we'll use a simplified approach:
        # The Speech Engine needs an engine ID. If you don't have one,
        # you can create it via the ElevenLabs dashboard or API.

        # SIMPLIFIED: For the hackathon demo, we'll document that
        # users should create a Speech Engine in the ElevenLabs dashboard
        # and set SPEECH_ENGINE_ID in their .env
        engine_id = os.environ.get("SPEECH_ENGINE_ID", "")

        if not engine_id:
            print("ℹ️  No SPEECH_ENGINE_ID set. Speech Engine requires an engine ID.")
            print("   Create one at: https://elevenlabs.io/app/speech-engine")
            print("   Then add SPEECH_ENGINE_ID=seng_xxx to your .env")
            return

        engine = await elevenlabs_async.speech_engine.get(engine_id)

        async def on_transcript(transcript, session):
            """Handle user speech transcript."""
            # transcript is a list of message objects with .role and .content
            messages = []
            for msg in transcript:
                role = "assistant" if msg.role == "agent" else msg.role
                messages.append({"role": role, "content": msg.content})

            if not messages:
                await session.send_response("Hello! Tell me about your business idea.")
                return

            if anthropic_client:
                try:
                    stream = anthropic_client.messages.stream(
                        model=CLAUDE_MODEL,
                        max_tokens=180,
                        system=SYSTEM_PROMPT,
                        messages=messages,
                    )
                    await session.send_response(stream)
                except Exception as e:
                    await session.send_response(f"Sorry, I had trouble thinking: {str(e)[:50]}")
            else:
                await session.send_response("I'm not configured with an AI brain right now. Check my API keys.")

        async def on_init(conversation_id, session):
            print(f"🎙️  Speech Engine session started: {conversation_id}")

        async def on_close(session):
            print(f"🎙️  Speech Engine session ended: {getattr(session, 'conversation_id', 'unknown')}")

        async def on_error(err, session):
            print(f"🎙️  Speech Engine error: {err}")

        # Start the server
        SPEECH_ENGINE_RUNNING = True
        print(f"✅ Speech Engine starting on port {SPEECH_ENGINE_PORT}...")

        await engine.serve(
            port=SPEECH_ENGINE_PORT,
            debug=(ENV == "development"),
            on_init=on_init,
            on_transcript=on_transcript,
            on_close=on_close,
            on_error=on_error,
        )

    except ImportError as e:
        print(f"ℹ️  ElevenLabs async SDK not available: {e}")
        print("   Install: pip install elevenlabs>=2.48.0")
    except Exception as e:
        print(f"⚠️  Speech Engine failed to start: {e}")
        traceback.print_exc()

# ── Manual WebSocket Fallback ────────────────────────────────────────────────
@app.websocket("/speech-engine")
async def speech_engine_ws(websocket: WebSocket):
    """Manual WebSocket fallback for when SDK Speech Engine isn't available."""
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_text()
            data = _json.loads(msg)

            if data.get("type") == "transcript":
                user_text = data.get("text", "")
                history = data.get("messages", [])

                messages = []
                for turn in history:
                    if turn.get("role") in ("user", "assistant"):
                        messages.append({"role": turn["role"], "content": turn.get("content", "")})
                if not messages or messages[-1]["role"] != "user":
                    messages.append({"role": "user", "content": user_text})

                if anthropic_client:
                    try:
                        with anthropic_client.messages.stream(
                            model=CLAUDE_MODEL, max_tokens=180, system=SYSTEM_PROMPT, messages=messages,
                        ) as stream:
                            full_text = ""
                            for text in stream.text_stream:
                                full_text += text
                                await websocket.send_text(_json.dumps({"type": "response_chunk", "text": text}))
                            await websocket.send_text(_json.dumps({"type": "response_end", "full_text": full_text}))
                    except Exception as e:
                        await websocket.send_text(_json.dumps({"type": "error", "message": str(e)}))
                else:
                    await websocket.send_text(_json.dumps({"type": "error", "message": "Anthropic not configured"}))

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_text(_json.dumps({"type": "error", "message": str(e)}))
            await websocket.close()
        except:
            pass

# ── HTTP Chat ─────────────────────────────────────────────────────────────────
@app.post("/chat")
async def chat(request: dict):
    if not anthropic_client:
        return JSONResponse({"error": "Anthropic API key not configured"}, status_code=500)

    messages = request.get("messages", [])
    if not messages:
        return JSONResponse({"error": "No messages"}, status_code=400)

    last_error = None
    for model in CLAUDE_MODELS:
        try:
            print(f"🤖 Trying: {model}")
            response = anthropic_client.messages.create(
                model=model,
                max_tokens=180,
                system=SYSTEM_PROMPT,
                messages=messages,
            )
            text = ""
            if response.content and len(response.content) > 0:
                if hasattr(response.content[0], 'text'):
                    text = response.content[0].text
                else:
                    text = str(response.content[0])
            if not text:
                text = "No response from AI."
            print(f"✅ {model} OK: {text[:60]}...")
            return {"response": text}
        except Exception as e:
            last_error = e
            err_str = str(e)
            print(f"⚠️  {model} failed: {err_str[:120]}")
            if "not_found" in err_str.lower() or "model" in err_str.lower():
                continue
            else:
                break

    err_msg = f"AI error: {str(last_error)}"
    print(f"❌ All failed: {err_msg}")
    return JSONResponse({"error": err_msg}, status_code=502)

# ── Token endpoint ────────────────────────────────────────────────────────────
@app.get("/conversation-token")
async def get_token():
    if not ELEVENLABS_API_KEY:
        return JSONResponse({"error": "ELEVENLABS_API_KEY not set"}, status_code=500)
    return {"api_key": ELEVENLABS_API_KEY, "voice_id": VOICE_ID, "mode": "dev_key"}

# ── Static & health ──────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("static/index.html") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(f"<h1>static/index.html not found</h1><p>CWD: {os.getcwd()}</p>")

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "domains": len(DOMAINS),
        "anthropic": anthropic_client is not None,
        "elevenlabs": bool(ELEVENLABS_API_KEY),
        "model": CLAUDE_MODEL,
        "speech_engine_running": SPEECH_ENGINE_RUNNING,
    }

@app.get("/debug/models")
async def debug_models():
    return {"models_to_try": CLAUDE_MODELS, "current_default": CLAUDE_MODEL}

@app.get("/domains/search")
async def domains_search(q: str):
    return {"query": q, "results": search_domains(q, top_k=10)}

# ── Print routes ─────────────────────────────────────────────────────────────
print("-" * 60)
print("ROUTES:")
for route in app.routes:
    path = getattr(route, "path", "N/A")
    methods = list(getattr(route, "methods", [])) if hasattr(route, "methods") else ["WS"]
    print(f"  {', '.join(methods):<10} {path}")
print("-" * 60)

# ── Entrypoint ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Start Speech Engine in background if possible
    if ELEVENLABS_API_KEY and DOMAIN_ENGINE_OK:
        try:
            # Try to start Speech Engine asynchronously
            loop = asyncio.get_event_loop()
            loop.create_task(start_speech_engine())
        except Exception as e:
            print(f"ℹ️  Could not start Speech Engine task: {e}")

    uvicorn.run("server:app", host="0.0.0.0", port=PORT, reload=(ENV=="development"))
