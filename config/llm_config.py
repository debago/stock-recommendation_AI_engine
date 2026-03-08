import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# -------------------------------------------------
# Load .env from project root reliably
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

# Load .env variables
load_dotenv(env_path)

# -------------------------------------------------
# Read environment variables
# -------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.2))
MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 1000))


# -------------------------------------------------
# Validate API Key
# -------------------------------------------------

if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError(
        "OPENAI_API_KEY not found. Please set it as environment variable."
    )

# Create a ChatOpenAI instance for GPT-3.5-turbo
# Initialize LLM
llm = ChatOpenAI(
    model=OPENAI_MODEL_NAME,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS,
    openai_api_key=OPENAI_API_KEY
)

# # Technical Agent LLM
# technical_llm = ChatOpenAI(
#     model_name=os.getenv("TECHNICAL_OPENAI_MODEL"),
#     temperature=0.2,
#     max_tokens=1000,
#     openai_api_key=os.getenv("TECHNICAL_OPENAI_API_KEY")
# )

# # Fundamental Agent LLM
# fundamental_llm = ChatOpenAI(
#     model=os.getenv("FUNDAMENTAL_OPENAI_MODEL"),
#     temperature=0.2,
#     max_tokens=1000,
#     openai_api_key=os.getenv("FUNDAMENTAL_OPENAI_API_KEY")
# )