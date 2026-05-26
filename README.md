# TerrificName AI — ElevenLabs Hack #10 Submission

**Voice-powered domain recommendation agent.** Speak your business idea → AI searches 412 premium domains → hear the perfect match in ~2 seconds.

**Live Demo:** [https://terrificname-ai.onrender.com](https://terrificname-ai.onrender.com)

**Video:** [YouTube Demo](YOUR_YOUTUBE_LINK_HERE)

---

## What It Does

1. **Tap the orb** and describe your business idea by voice (e.g., *"I need a fintech startup domain for crypto payments"*)
2. **Web Speech API** transcribes your speech in the browser
3. **FastAPI backend** sends your query + full 412-domain portfolio to Claude 3.5 Sonnet
4. **Claude reasons** over categories, tags, and brandability to return the top 3 matches
5. **ElevenLabs TTS** voices the recommendation back naturally through the browser

## Demo

[Insert GIF or screenshot of orb + conversation panel]

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Voice STT | Web Speech API (browser-native) |
| Voice TTS | ElevenLabs API |
| Backend | FastAPI (Python) |
| AI Reasoning | Claude 3.5 Sonnet |
| Frontend | Vanilla HTML / CSS / JS (no build step) |
| Hosting | Render (free tier) |
| Monitoring | UptimeRobot |

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/pashz/terrificname-ai.git
cd terrificname-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
cp .env.example .env
# Edit .env with your keys:
#   ANTHROPIC_API_KEY=sk-ant-...
#   ELEVENLABS_API_KEY=sk_...
#   ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Rachel (default)

# 4. Run the server
python server.py

# 5. Open http://localhost:8000 in Chrome
# Tap the orb → speak → hear domain recommendations
```

## Project Structure

```
terrificname-ai/
├── server.py              # FastAPI server (/chat, /health, /docs)
├── domain_engine.py       # Claude reasoning + domains.json loader
├── data/
│   └── domains.json       # 412 categorized premium domains
├── static/
│   └── index.html         # Voice-enabled frontend
├── requirements.txt
└── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Main query endpoint — send text, get AI response + TTS audio |
| `/health` | GET | Health check for monitoring |
| `/docs` | GET | Auto-generated Swagger/OpenAPI docs |
| `/conversation-token` | GET | Token for conversation state |

## Deployment

### Render (Recommended — Free Tier)
1. Connect your GitHub repo to Render
2. Set environment variables in Render dashboard
3. Auto-deploys on every push
4. Note: Free tier spins down after 15 min inactivity (first request may take ~30s to wake)

### Railway
- $5 free credit, no sleep mode
- Better for demo day traffic

### Fly.io
- `fly launch` → free allowances available

## Browser Support

- **Chrome**: Full voice support (Web Speech API)
- **Edge/Opera/Safari**: Text mode fallback by design
- **Mobile Chrome**: Supported

## Fallback Mode

If voice input fails or browser is unsupported, the frontend automatically switches to text mode:
- Type your business idea
- Backend returns Claude response via HTTP
- Frontend auto-plays ElevenLabs TTS via REST API

## Keep Alive

See [KEEP_ALIVE.md](KEEP_ALIVE.md) for the 1-line ping setup to prevent Render free tier spin-down.

## License

MIT License — see [LICENSE](LICENSE) file.

---

Built for [ElevenLabs Hack #10](https://elevenlabs.io/hackathon) — Speech Engine category.
