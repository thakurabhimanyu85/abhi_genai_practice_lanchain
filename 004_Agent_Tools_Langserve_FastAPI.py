from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.agents.factory import create_agent
from langchain_core.tools import tool
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel
from fastapi import FastAPI
from langserve import add_routes
import uvicorn


# ------------------ MODEL ------------------
model = init_chat_model(
    model="llama-3.1-8b-instant",
    model_provider="groq",
    temperature=0.7
)


class InputSchema(BaseModel):
    input: str
# ------------------ TOOLS ------------------
@tool
def get_topic_info(topic: str) -> str:
    """Get information about a specific topic"""
    return f"Information about {topic}: This is a helpful summary."


@tool
def search_web(query: str) -> str:
    """Search the web for information"""
    return f"Search results for '{query}': Found relevant information..."


@tool
def get_definition(word: str) -> str:
    """Get the definition of a word"""
    return f"Definition of '{word}': A concise meaning of the term."


tools = [get_topic_info, search_web, get_definition]


# ------------------ AGENT ------------------
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="You are a helpful assistant with access to tools. Use tools when needed."
)


# ------------------ INPUT ADAPTER ------------------
def adapt_input(x):
    return {
        "messages": [
            {"role": "user", "content": x["input"]}
        ]
    }


# ------------------ OUTPUT ADAPTER ------------------
def adapt_output(x):
    try:
        return x["model"]["messages"][-1].content
    except Exception:
        return str(x)
# ------------------ FINAL PIPELINE ------------------
final_agent = (
    RunnableLambda(adapt_input)
    | agent
    | RunnableLambda(adapt_output)
)


# ------------------ FASTAPI ------------------
app = FastAPI(
    title="Chatbot with Tools",
    version="1.0",
    description="LangServe agent with simple textbox UI"
)


# ------------------ LANGSERVE ROUTES ------------------
add_routes(app, final_agent, path="/langserve_agent_with_tools",input_type=InputSchema )   


# ------------------ RUN SERVER ------------------
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8004)