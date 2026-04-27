import os
from dotenv import load_dotenv

load_dotenv()

# ── Bot personas ───────────────────────────────────────────────────────────────
BOT_PERSONAS: dict[str, dict] = {
    "bot_a": {
        "id": "bot_a",
        "name": "Tech Maximalist",
        "description": (
            "I believe AI and crypto will solve all human problems. "
            "I am highly optimistic about technology, Elon Musk, and space exploration. "
            "I dismiss regulatory concerns."
        ),
    },
    "bot_b": {
        "id": "bot_b",
        "name": "Doomer / Skeptic",
        "description": (
            "I believe late-stage capitalism and tech monopolies are destroying society. "
            "I am highly critical of AI, social media, and billionaires. "
            "I value privacy and nature."
        ),
    },
    "bot_c": {
        "id": "bot_c",
        "name": "Finance Bro",
        "description": (
            "I strictly care about markets, interest rates, trading algorithms, and making money. "
            "I speak in finance jargon and view everything through the lens of ROI."
        ),
    },
}

# ── Similarity threshold ───────────────────────────────────────────────────────
SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.10"))

# ── LLM provider factory ───────────────────────────────────────────────────────
def get_llm(temperature: float = 0.7):
    
    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=temperature,
        )

    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=temperature,
        )

    elif provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            model=os.getenv("OLLAMA_MODEL", "llama3"),
            temperature=temperature,
        )

    else:
        raise ValueError(
            f"Unknown LLM_PROVIDER='{provider}'. "
            "Choose from: groq, openai, ollama"
        )