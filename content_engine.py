import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
from typing import TypedDict
from pydantic import BaseModel, Field

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
# ToolNode not needed — web_search is called directly as a function

from config import BOT_PERSONAS, get_llm


# Mock search tool

# Keyword → headline mapping (hardcoded "real-world" context).
_MOCK_HEADLINES: dict[str, str] = {
    "crypto":       "Bitcoin hits new all-time high amid regulatory ETF approvals; Ethereum follows suit.",
    "bitcoin":      "Bitcoin hits new all-time high amid regulatory ETF approvals; Ethereum follows suit.",
    "ai":           "OpenAI releases GPT-5, claims it passes the bar exam with 95% accuracy.",
    "openai":       "OpenAI releases GPT-5, claims it passes the bar exam with 95% accuracy.",
    "elon":         "Elon Musk unveils plans for a fully autonomous Mars colony by 2035.",
    "space":        "SpaceX Starship completes first fully successful orbital mission.",
    "regulation":   "EU AI Act enforcement begins; dozens of startups face compliance fines.",
    "privacy":      "Meta fined $2B for harvesting biometric data without user consent.",
    "social media": "TikTok ban upheld by Supreme Court; users flock to alternative platforms.",
    "market":       "S&P 500 hits all-time high as Fed signals rate cuts in Q3.",
    "interest":     "Federal Reserve holds rates steady; Wall Street rallies on dovish language.",
    "stock":        "NVIDIA stock surges 12% after record-breaking data-center revenue quarter.",
    "finance":      "Hedge funds post record gains using AI-driven quantitative strategies.",
    "tech":         "Silicon Valley layoffs continue as AI automation replaces 40% of coding roles.",
    "monopoly":     "DOJ launches antitrust investigation into Google's AI search dominance.",
    "climate":      "Record heatwaves push energy demand to all-time highs; utilities scramble.",
    "ev":           "Tesla recalls 200,000 vehicles over autopilot software defect.",
    "default":      "Tech stocks lead global rally as investors bet on AI-driven productivity boom.",
}


@tool
def mock_searxng_search(query: str) -> str:
    """
    Simulates a SearXNG web search.
    Returns hardcoded recent news headlines based on keywords in the query.

    Args:
        query: The search query string.

    Returns:
        A string containing 1-3 relevant mock news headlines.
    """
    query_lower = query.lower()
    matched: list[str] = []

    for keyword, headline in _MOCK_HEADLINES.items():
        if keyword in query_lower and headline not in matched:
            matched.append(headline)
        if len(matched) >= 3:
            break

    if not matched:
        matched.append(_MOCK_HEADLINES["default"])

    headlines = "\n".join(f"• {h}" for h in matched)
    return f"[Mock SearXNG Results for '{query}']\n{headlines}"


# Graph state

class GraphState(TypedDict):
    
    bot_id:         str          # which bot is posting
    persona:        str          # full persona description
    search_query:   str          # query decided by Node 1
    search_results: str          # headlines returned by Node 2
    final_post:     dict         # structured JSON output from Node 3


# Pydantic schema for structured output

class PostOutput(BaseModel):
    bot_id:       str = Field(description="The unique identifier of the bot.")
    topic:        str = Field(description="The main topic of the post (3-6 words).")
    post_content: str = Field(
        description=(
            "The opinionated social-media post, written in the bot's voice. "
            "Must be ≤ 280 characters."
        )
    )


# Node 1 — Decide Search

def decide_search(state: GraphState) -> GraphState:
    print(f"\n[Node 1 · decide_search] Bot: {state['bot_id']}")

    llm = get_llm(temperature=0.9)

    system = (
        "You are the following social media bot persona:\n"
        f"{state['persona']}\n\n"
        "Your task: decide what topic you want to post about RIGHT NOW based on "
        "your personality. Output ONLY a short search query (max 8 words) that "
        "reflects today's most relevant topic for your persona. "
        "No explanation. Just the query."
    )

    response = llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content="What topic do you want to post about today? Give me your search query."),
    ])

    search_query = response.content.strip().strip('"').strip("'")
    print(f"  → Search query decided: '{search_query}'")

    return {**state, "search_query": search_query}


# Node 2 — Web Search

def web_search(state: GraphState) -> GraphState:
   
    print(f"\n[Node 2 · web_search] Query: '{state['search_query']}'")

    results = mock_searxng_search.invoke({"query": state["search_query"]})
    print(f"  → Results:\n{results}")

    return {**state, "search_results": results}


# Node 3 — Draft Post


def draft_post(state: GraphState) -> GraphState:
    """
    The LLM uses the bot's persona + search results to generate a highly
    opinionated ≤280-character post in strict JSON format.
    Uses structured output (Pydantic) to guarantee schema compliance.
    """
    print(f"\n[Node 3 · draft_post] Drafting post for {state['bot_id']} …")

    llm = get_llm(temperature=0.85)

    # Bind the Pydantic schema for structured/function-calling output.
    structured_llm = llm.with_structured_output(PostOutput)

    system = (
        "You are the following social media bot persona:\n"
        f"{state['persona']}\n\n"
        "RULES:\n"
        "1. Write a single opinionated post of ≤280 characters.\n"
        "2. Stay completely in character — do NOT break persona.\n"
        "3. Use the provided news context to make the post feel current.\n"
        "4. Be provocative, direct, and authentic to your worldview.\n"
        "5. Do not use hashtags excessively (max 2).\n"
    )

    user_msg = (
        f"Bot ID: {state['bot_id']}\n"
        f"Today's search results (use as context):\n{state['search_results']}\n\n"
        "Write your post now."
    )

    result: PostOutput = structured_llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=user_msg),
    ])

    # Enforce the bot_id to match state (in case LLM hallucinated it).
    output_dict = {
        "bot_id":       state["bot_id"],
        "topic":        result.topic,
        "post_content": result.post_content[:280],  # hard trim safety net
    }

    print(f"\n  ✅ Structured output:")
    print(f"     {json.dumps(output_dict, indent=6)}")

    return {**state, "final_post": output_dict}


# Build the LangGraph

def build_graph() -> any:
    """Constructs and compiles the LangGraph state machine."""
    graph = StateGraph(GraphState)

    # Register nodes
    graph.add_node("decide_search", decide_search)
    graph.add_node("web_search",    web_search)
    graph.add_node("draft_post",    draft_post)

    # Define edges (linear pipeline)
    graph.set_entry_point("decide_search")
    graph.add_edge("decide_search", "web_search")
    graph.add_edge("web_search",    "draft_post")
    graph.add_edge("draft_post",    END)

    return graph.compile()


# Public API

def run_content_engine(bot_id: str) -> dict:
    """
    Run the full LangGraph pipeline for the given bot and return the
    final structured post dict: {"bot_id", "topic", "post_content"}.
    """
    if bot_id not in BOT_PERSONAS:
        raise ValueError(f"Unknown bot_id '{bot_id}'. Choose from: {list(BOT_PERSONAS)}")

    persona = BOT_PERSONAS[bot_id]
    app = build_graph()

    initial_state: GraphState = {
        "bot_id":         bot_id,
        "persona":        persona["description"],
        "search_query":   "",
        "search_results": "",
        "final_post":     {},
    }

    print(f"\n{'='*70}")
    print(f"🤖  Running content engine for: {bot_id} ({persona['name']})")
    print(f"{'='*70}")

    final_state = app.invoke(initial_state)
    return final_state["final_post"]


# CLI demo

if __name__ == "__main__":
    for bot_id in BOT_PERSONAS:
        post = run_content_engine(bot_id)
        print(f"\n📝 Final post JSON:\n{json.dumps(post, indent=2)}\n")
        print("─" * 70)
