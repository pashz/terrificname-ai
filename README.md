# TerrificName AI — ElevenLabs Hack #10 Submission

**Voice-powered domain recommendation agent.** Speak your business idea → AI searches 412 premium domains → hears the perfect match in ~2 seconds.

## What it does
- User describes a business idea by voice (e.g., "I need a fintech startup domain")
- ElevenLabs Speech Engine transcribes speech → sends to our FastAPI backend
- Claude reasons over the full 412-domain portfolio and returns top 3 matches
- ElevenLabs voices the recommendation back naturally with interruption support

## Tech stack
- **Voice**: ElevenLabs Speech Engine (STT + TTS + turn-taking)
- **Backend**: FastAPI + Python
- **Reasoning**: Claude 3.5 Sonnet with full portfolio context
- **Frontend**: Vanilla HTML/JS (no build step)

## Quick start

```bash
# 1. Clone / unzip project
cd terrificname-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
cp .env.example .env
# Edit .env with your keys:
#   ANTHROPIC_API_KEY=sk-ant-...
#   ELEVENLABS_API_KEY=sk_...
#   ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Rachel (default)

# 4. Run server
python server.py

# 5. Open http://localhost:8000 in browser
# Tap the orb → speak → hear domain recommendations
```

## Project structure
```
terrificname-ai/
├── server.py              # FastAPI + Speech Engine WebSocket
├── domain_engine.py       # Claude reasoning + 412-domain database
├── data/
│   └── domains.json       # Full categorized portfolio
├── static/
│   └── index.html         # Demo frontend
├── requirements.txt
└── README.md
```

## Hackathon scoring checklist
- [ ] Project submitted on ElevenHacks portal (Thu 28 May 17:00 UTC)
- [ ] Cover image uploaded (1280×720, bold text, "wow" moment)
- [ ] Repo URL linked (GitHub public repo)
- [ ] Live demo URL linked (Render / Railway / Fly.io)
- [ ] 60-90 second video uploaded (5-second hook, captions)
- [ ] Social posts on X, LinkedIn, Instagram, TikTok (+200 pts)

## Keep Alive (Render Free Tier)

See [KEEP_ALIVE.md](KEEP_ALIVE.md) for the 1-line ping setup.

## Deployment (free tier)
**Render**: Connect GitHub repo → auto-deploy on push → free tier sleeps after 15 min (fine for judging)
**Railway**: $5 free credit → no sleep → better for demo day
**Fly.io**: `fly launch` → free allowances

## Fallback mode
If Speech Engine WebSocket has SDK issues, the frontend auto-switches to text mode:
- User types business idea
- Backend returns Claude response via HTTP
- Frontend auto-plays ElevenLabs TTS via REST API
- Still a valid demo — judges care about functionality, not transport layer purity.
