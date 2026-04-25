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

tools = []

# Create the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Use tools when the user asks for information. If the user just wants a simple answer, respond directly without using tools."),
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
add_routes(app, agent_executor, path="/langserve_agent_No_Tools")

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8003)


#create_agent does not accept a human_prompt argument. It only takes system_prompt
# country = "India"

# response = agent_executor.invoke(
#     {"input": f"What is the capital of {country}?"}
# )
# print(response["output"])