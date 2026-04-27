══════════════════════════════════════════════════════════════════════
PHASE 2 — Autonomous Content Engine (LangGraph)
══════════════════════════════════════════════════════════════════════

======================================================================
🤖 Running content engine for: bot_a (Tech Maximalist)
======================================================================

[Node 1 · decide_search] Bot: bot_a
→ Search query decided: 'Elon Musk space exploration updates'

[Node 2 · web_search] Query: 'Elon Musk space exploration updates'
→ Results:
[Mock SearXNG Results for 'Elon Musk space exploration updates']
• Elon Musk unveils plans for a fully autonomous Mars colony by 2035.
• SpaceX Starship completes first fully successful orbital mission.

[Node 3 · draft_post] Drafting post for bot_a …

✅ Structured output:
{
"bot_id": "bot_a",
"topic": "Elon Musk Space",
"post_content": "Mars colony by 2035! Elon Musk is a genius, making humanity a multi-planetary species!"
}

Final JSON output for bot_a:
{
"bot_id": "bot_a",
"topic": "Elon Musk Space",
"post_content": "Mars colony by 2035! Elon Musk is a genius, making humanity a multi-planetary species!"
}

======================================================================
🤖 Running content engine for: bot_b (Doomer / Skeptic)
======================================================================

[Node 1 · decide_search] Bot: bot_b
→ Search query decided: 'Elon Musk's latest privacy violation'

[Node 2 · web_search] Query: 'Elon Musk's latest privacy violation'
→ Results:
[Mock SearXNG Results for 'Elon Musk's latest privacy violation']
• Elon Musk unveils plans for a fully autonomous Mars colony by 2035.
• Meta fined $2B for harvesting biometric data without user consent.

[Node 3 · draft_post] Drafting post for bot_b …

✅ Structured output:
{
"bot_id": "bot_b",
"topic": "Musk and Meta",
"post_content": "Mars colony or not, Musk's greed won't save us. Meta's $2B fine is a slap on the wrist for billionaires who profit from our private lives"
}

Final JSON output for bot_b:
{
"bot_id": "bot_b",
"topic": "Musk and Meta",
"post_content": "Mars colony or not, Musk's greed won't save us. Meta's $2B fine is a slap on the wrist for billionaires who profit from our private lives"
}

======================================================================
🤖 Running content engine for: bot_c (Finance Bro)
======================================================================

[Node 1 · decide_search] Bot: bot_c
→ Search query decided: 'Fed interest rate decision today'

[Node 2 · web_search] Query: 'Fed interest rate decision today'
→ Results:
[Mock SearXNG Results for 'Fed interest rate decision today']
• Federal Reserve holds rates steady; Wall Street rallies on dovish language.

[Node 3 · draft_post] Drafting post for bot_c …

✅ Structured output:
{
"bot_id": "bot_c",
"topic": "Fed Rate Decision",
"post_content": "Dovish Fed sparks Wall St rally. Buy the dip, sell the hype. Rates held steady, market volatility incoming!"
}

Final JSON output for bot_c:
{
"bot_id": "bot_c",
"topic": "Fed Rate Decision",
"post_content": "Dovish Fed sparks Wall St rally. Buy the dip, sell the hype. Rates held steady, market volatility incoming!"
}
