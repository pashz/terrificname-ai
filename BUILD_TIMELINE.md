# 3-Day Emergency Build Timeline — TerrificName AI

**Deadline**: Thu 28 May, 17:00 UTC (~72 hours from now)
**Commitment**: 40 hrs/week ≈ 12 hours over 3 days (4 hrs/day + 8-hr push day)

---

## Day 1 — Tuesday (Today) — FOUNDATION [4 hrs]

**Hour 1: Setup & Keys**
- [ ] Export ElevenLabs API key + claim free Creator Plan
- [ ] Export Anthropic API key (Claude)
- [ ] Create GitHub repo `terrificname-ai` (public)
- [ ] Push initial code skeleton (server.py, domain_engine.py, static/, data/)
- [ ] Test `pip install -r requirements.txt` locally

**Hour 2: Backend Core**
- [ ] Verify `domains.json` loads all 412 domains correctly
- [ ] Test Claude API call with full portfolio context (check token count)
- [ ] Verify response quality: "I need a fintech domain" → should return koinpay.com, moneyarc.com, etc.
- [ ] Wire up `/chat` HTTP endpoint (fallback mode)

**Hour 3: Speech Engine Integration**
- [ ] Test Speech Engine SDK import (`from elevenlabs.speech_engine import SpeechEngine`)
- [ ] If import fails: verify `pip install elevenlabs>=1.0.0` and check SDK version
- [ ] Wire up WebSocket endpoint (manual fallback is already coded — test it)
- [ ] Test full loop: speak → transcript → Claude → voice response

**Hour 4: Frontend Polish**
- [ ] Test index.html loads, orb animates, transcript renders
- [ ] Test text fallback mode (type query → get response → auto-play TTS)
- [ ] Push all code to GitHub
- [ ] Deploy to Render/Railway (get live URL for submission form)

**End of Day 1 deliverable**: Working local demo + live URL + GitHub repo.

---

## Day 2 — Wednesday — DEMO & VIDEO [4 hrs]

**Hour 1: Record Demo Video**
- [ ] Write 5-second hook script (memorize it)
- [ ] Record 3-5 demo takes in coffee shop or well-lit room
- [ ] Best test query: *"I need a fintech startup domain"* → AI should respond with koinpay.com
- [ ] Record B-roll: finger tapping orb, code screen, domain list scroll

**Hour 2: Edit Video**
- [ ] Import to CapCut (free)
- [ ] Auto-captions ON (white text, black outline)
- [ ] Add music (subtle, from ElevenLabs Music or CapCut library)
- [ ] 5-second hook rule: cut anything before the first sentence
- [ ] Export vertical 9:16 AND horizontal 16:9

**Hour 3: Write Submission**
- [ ] ElevenHacks portal: fill project description
- [ ] Write 2-paragraph "What I built" (see script below)
- [ ] Upload cover image (1280×720, bold text, orb screenshot)
- [ ] Link GitHub repo + live demo URL
- [ ] Upload video to YouTube (unlisted) → paste link

**Hour 4: Social Blitz (+200 pts)**
- [ ] X: Post hook + demo video
- [ ] LinkedIn: Professional angle post
- [ ] Instagram: Reel with caption
- [ ] TikTok: Video with trending audio if possible
- [ ] Reply to all comments for 30 min (algorithm boost)

**Submission description template**:
> TerrificName AI is a voice-powered domain broker. Users describe their business idea by voice, and the agent searches a curated portfolio of 412 premium domains collected over 14 years. It returns the top 2-3 matches with reasoning, voiced naturally via ElevenLabs Speech Engine.
>
> I used Speech Engine because it handles the full voice lifecycle — STT, TTS, turn-taking, and interruption detection — while letting me bring my own LLM (Claude 3.5 Sonnet) and domain knowledge base. The SDK's built-in Anthropic stream extraction meant zero adapter code.
>
> This solves a real pain: domain search is creative and iterative, but every existing tool forces typing. Voice removes friction and makes exploration feel like a conversation with an expert broker.

**End of Day 2 deliverable**: Video done, submission form filled, social posts live.

---

## Day 3 — Thursday — SUBMIT & SURVIVE [4 hrs]

**Hour 1: Final QA**
- [ ] Test live demo URL on mobile (judges will test on phone)
- [ ] Test 3 different voice queries:
  1. "I need a health and wellness brand"
  2. "Find me a real estate domain"
  3. "Something for a tech startup"
- [ ] Verify responses are under 60 words and natural-sounding
- [ ] Fix any bugs, redeploy

**Hour 2: Buffer & Polish**
- [ ] Add README screenshot/GIF to GitHub repo
- [ ] Add MIT license file (1 click on GitHub)
- [ ] Verify all submission fields are complete
- [ ] Double-check social posts have `@elevenlabsio` and `#ElevenHacks`

**Hour 3: Pre-submission social push**
- [ ] Post "final hours" reminder on X and LinkedIn
- [ ] Engage with other hackers' posts (community vote = +200 pts for "Most Popular")
- [ ] Share in relevant Discords/Slacks (Indie Hackers, AI builders)

**Hour 4: SUBMIT**
- [ ] Submit on ElevenHacks portal BEFORE 16:00 UTC (1-hour buffer)
- [ ] Screenshot confirmation page
- [ ] Celebrate. You've shipped.

**Thu 17:00 UTC**: Deadline passes. Project locked.
**Tue 2 Jun, 17:00 UTC**: Winners announced.

---

## Kill Criteria (If Things Go Wrong)

| Scenario | Fallback |
|----------|----------|
| Speech Engine SDK won't import | Use manual WebSocket fallback (already coded) |
| WebSocket unstable | Switch frontend to text mode + TTS REST API (already coded) |
| Claude context too long for 412 domains | Trim to top 200 domains by category relevance |
| Deploy platform fails | Use ngrok tunnel for demo URL (temporary but works) |
| Video too hard | Screen recording + voiceover using ElevenLabs TTS |
| No time for social | Batch schedule via Buffer/Typefully (free tier) |

---

## Hour-by-Hour Priority (If You Only Have 8 Hours Total)

1. **Hour 1–2**: Backend works locally (Claude + domains)
2. **Hour 3**: Frontend loads and shows responses
3. **Hour 4**: Deploy live URL (Render/Railway)
4. **Hour 5**: Record 60-second screen demo video
5. **Hour 6**: Submit project form with repo + URL + video
6. **Hour 7**: Post on X + LinkedIn (highest value platforms)
7. **Hour 8**: Post on Instagram + TikTok (completes +200 pts)

**Minimum viable submission**: Live URL + repo + 60s video + 4 social posts. Everything else is polish.
