GRID07 — AI Cognitive Routing & RAG — Full Demo

══════════════════════════════════════════════════════════════════════
PHASE 1 — Vector-Based Persona Matching (The Router)
══════════════════════════════════════════════════════════════════════

📨 POST: OpenAI just released a new model that might replace junior developers.
Expected: bot_a (tech/AI topic → Tech Maximalist, maybe Doomer)
Similarities:
[Router] Embedding and storing bot personas …
[Router] Loading embedding model 'all-MiniLM-L6-v2' …
[Router] Embedding model loaded ✓
✓ bot_a (Tech Maximalist) stored
✓ bot_b (Doomer / Skeptic) stored
✓ bot_c (Finance Bro) stored
[Router] All personas indexed ✓

[Router] bot_a (Tech Maximalist) → similarity=0.2198 ✅ MATCHED
[Router] bot_b (Doomer / Skeptic) → similarity=0.1271 ✅ MATCHED
[Router] bot_c (Finance Bro) → similarity=0.0789 ❌ below threshold

✅ Routed to 2 bot(s):
→ bot_a (Tech Maximalist) sim=0.2198
→ bot_b (Doomer / Skeptic) sim=0.1271

📨 POST: Bitcoin hits a new all-time high as institutional investors pile in.
Expected: bot_c (finance topic → Finance Bro)
Similarities:
[Router] bot_c (Finance Bro) → similarity=0.2924 ✅ MATCHED
[Router] bot_a (Tech Maximalist) → similarity=0.2674 ✅ MATCHED
[Router] bot_b (Doomer / Skeptic) → similarity=0.2400 ✅ MATCHED

✅ Routed to 3 bot(s):
→ bot_c (Finance Bro) sim=0.2924
→ bot_a (Tech Maximalist) sim=0.2674
→ bot_b (Doomer / Skeptic) sim=0.2400

📨 POST: Big Tech companies are lobbying against privacy laws to harvest user data.
Expected: bot_b (anti-tech topic → Doomer/Skeptic)
Similarities:
[Router] bot_b (Doomer / Skeptic) → similarity=0.3432 ✅ MATCHED
[Router] bot_a (Tech Maximalist) → similarity=0.3324 ✅ MATCHED
[Router] bot_c (Finance Bro) → similarity=0.1213 ✅ MATCHED

✅ Routed to 3 bot(s):
→ bot_b (Doomer / Skeptic) sim=0.3432
→ bot_a (Tech Maximalist) sim=0.3324
→ bot_c (Finance Bro) sim=0.1213

📨 POST: The Federal Reserve raises interest rates by 50 basis points today.
Expected: bot_c (macroeconomics → Finance Bro)
Similarities:
[Router] bot_c (Finance Bro) → similarity=0.2508 ✅ MATCHED
[Router] bot_a (Tech Maximalist) → similarity=0.0579 ❌ below threshold
[Router] bot_b (Doomer / Skeptic) → similarity=-0.0020 ❌ below threshold

✅ Routed to 1 bot(s):
→ bot_c (Finance Bro) sim=0.2508

📨 POST: SpaceX successfully launches Starship on an orbital mission.
Expected: bot_a (space/tech → Tech Maximalist)
Similarities:
[Router] bot_a (Tech Maximalist) → similarity=0.1285 ✅ MATCHED
[Router] bot_c (Finance Bro) → similarity=0.0787 ❌ below threshold
[Router] bot_b (Doomer / Skeptic) → similarity=-0.0260 ❌ below threshold

✅ Routed to 1 bot(s):
→ bot_a (Tech Maximalist) sim=0.1285
