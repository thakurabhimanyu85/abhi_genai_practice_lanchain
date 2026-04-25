from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI
from langserve import add_routes
import uvicorn

model = init_chat_model(model="llama-3.1-8b-instant", model_provider="groq", temperature=0.7)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "Tell me about {topic}."),
    ]
)

# Create the agent by chaining prompt and model
agent = prompt | model # Creates a runnable pipeline: user input → format with prompt → send to model → get response

# Simple input → prompt → LLM → output (no tools)	Chains (prompt \| model)
# LLM needs to call external functions/APIs	create_agent() + toolsel

# Initialize FastAPI app
app = FastAPI(
    title="Chatbot for simple query using LLM Call Chain",
    version="1.0",
    description="A Chatbot for simple query using LangChain and LangServe"
)

# Add routes for the runnable chain
add_routes(app, agent, path="/langserve_agent_llm_call_chain")

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)


#create_agent does not accept a human_prompt argument. It only takes system_prompt
# topic = "Python programming"

# response = agent.invoke(
#     {"messages": [{"role": "user", "content": f"Tell me about {topic}?"}]}
# )
# print(response["messages"])
# The agent is returning a dictionary with a "messages" list, and each item in that list is a HumanMessage or AIMessage object. Those objects have the .content attribute which contains the text of the message. So to get the content of each message, you can loop through the messages and print the .content attribute of each one.
# for msg in response["messages"]:
#     print(msg.content)
# print(response["messages"][0])
# print(response["messages"][1].content)
# response = model.invoke(prompt.format_messages(country="France"))
#print(prompt.invoke(prompt.format_messages(country="India"))) # formats the template into a structured message.
#print(agent.invoke({"country": "India"}))