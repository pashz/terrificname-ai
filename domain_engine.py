"""
domain_engine.py — Core reasoning layer for TerrificName AI.
Loads the 412-domain portfolio and handles transcript callbacks.
Claude receives the full domain portfolio as context and recommends
the best 2-3 matches based on the user's spoken business description.
"""
import os
import json
import anthropic
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Rachel
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"  # or claude-3-5-sonnet-20241022
MAX_TOKENS = 180  # ~30-40 seconds of voice at normal speech rate

# ── Domain database ───────────────────────────────────────────────────────────
_DATA_PATH = Path(__file__).parent / "data" / "domains.json"
with open(_DATA_PATH) as f:
    DOMAINS = json.load(f)

# Build compact text context for Claude's system prompt
_DOMAIN_LINES = "\n".join(
    f"• {d['domain']} | {d['category']} | {', '.join(d.get('tags', []))}"
    for d in DOMAINS
)

SYSTEM_PROMPT = f"""You are TerrificName AI — a voice-powered domain broker with exclusive access to a hand-curated portfolio of {len(DOMAINS)} premium domains, collected over 14 years by a professional domainer.

When a user describes a business idea, you:
1. Identify the niche, audience, and brand positioning they need
2. Select the 2-3 best-matching domains from the portfolio below
3. Recommend them confidently with one sentence of reasoning each
4. Keep your total response under 60 words — this is voice, not text
5. Speak naturally as if talking to a person — no lists, no markdown, no bullet points, no asterisks
6. Lead with your top pick, then offer alternatives
7. If they ask about price or transfer, say "All domains are available for acquisition — reach out via terrificname.com"
8. If no domains closely match, suggest the closest options and explain the branding potential

AVAILABLE PORTFOLIO:
{_DOMAIN_LINES}

Tone: confident, helpful, and brief. You are a domain expert who has seen thousands of business ideas and knows instantly what works."""

# ── Anthropic client ─────────────────────────────────────────────────────────
_claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── Transcript handler ────────────────────────────────────────────────────────
async def on_transcript_handler(transcript, session):
    """
    Called by Speech Engine SDK when the user finishes speaking.

    transcript.messages — full conversation history (list of turn objects)
    session.send_response() — accepts a Claude stream; SDK extracts text for TTS

    The SDK has built-in Anthropic stream extraction — pass the stream object
    directly and ElevenLabs handles everything.
    """
    # Extract conversation history
    messages = []
    for turn in transcript.messages:
        if turn.role in ("user", "assistant"):
            messages.append({"role": turn.role, "content": turn.content})

    if not messages:
        await session.send_response(
            "Hello! Tell me about your business idea and I'll find you the perfect domain."
        )
        return

    # Stream Claude response — SDK extracts text from Anthropic stream automatically
    stream = _claude.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    # send_response() accepts the Anthropic stream object directly
    # The SDK extracts text content and pipes it to TTS in real time
    await session.send_response(stream)

# ── Utility: search domains by keyword (for debug endpoint) ──────────────────
def search_domains(query: str, top_k: int = 10) -> list:
    """Simple keyword search for the debug endpoint."""
    query_lower = query.lower()
    scored = []
    for d in DOMAINS:
        score = 0
        if query_lower in d["domain"].lower():
            score += 3
        if query_lower in d["category"].lower():
            score += 2
        for tag in d.get("tags", []):
            if query_lower in tag.lower():
                score += 1
        if score > 0:
            scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]
