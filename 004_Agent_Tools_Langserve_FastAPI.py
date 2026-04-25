from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from fastapi import FastAPI
from langserve import add_routes
import uvicorn

model = init_chat_model(model="llama-3.1-8b-instant", model_provider="groq", temperature=0.7)

# Define tools that the agent can use
@tool
def get_topic_info(topic: str) -> str:
    """Get information about a specific topic"""
    # Placeholder - in real app, this would call an API or database
    return f"Information about {topic}: This is a helpful summary."

@tool
def search_web(query: str) -> str:
    """Search the web for information"""
    # Placeholder - in real app, this would call a search API like Tavily
    return f"Search results for '{query}': Found relevant information..."

@tool
def get_definition(word: str) -> str:
    """Get the definition of a word"""
    return f"Definition of '{word}': A concise meaning of the term."

tools = [get_topic_info, search_web, get_definition]

# Create the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant with access to tools. Use the tools when the user asks for information."),
        ("human", "{input}"),
    ]
)

# Create the agent
agent = create_tool_calling_agent(model, tools, prompt)

# Create AgentExecutor to run the agent
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Initialize FastAPI app
app = FastAPI(
    title="Chatbot with Tools",
    version="1.0",
    description="A Chatbot with tool-calling capabilities using LangChain and LangServe"
)

# Add routes for the agent executor
add_routes(app, agent_executor, path="/langserve_agent_with_tools")

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8004)


#create_agent does not accept a human_prompt argument. It only takes system_prompt
# country = "India"

# response = agent_executor.invoke(
#     {"input": f"What is the capital of {country}?"}
# )
# print(response["output"])