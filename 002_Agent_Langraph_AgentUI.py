from click import prompt
from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent

model=init_chat_model(model="llama-3.1-8b-instant",model_provider="groq",  temperature=0.7)
system_prompt = "You are a helpful assistant."
human_prompt = "What is the capital of {country}?"


# agent = prompt | model
agent = create_agent(
    model=model,
    system_prompt=system_prompt
)

#create_agent does not accept a human_prompt argument. It only takes system_prompt
# country = "India"

# response = agent.invoke(
#     {"messages": [{"role": "user", "content": f"What is the capital of {country}?"}]}
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