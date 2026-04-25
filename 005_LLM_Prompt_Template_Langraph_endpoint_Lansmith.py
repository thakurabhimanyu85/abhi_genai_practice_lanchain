from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.factory import create_agent

model=init_chat_model(model="llama-3.1-8b-instant",model_provider="groq",  temperature=0.7)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "Tell me about {topic}."),
    ]
)
# agent=create_agent(model=model, system_prompt=prompt)
# system_prompt expects string not prompt template, so we need to convert the prompt template into a string. We can do this by using the format_messages method of the prompt template, which will return a list of messages that we can then join into a single string.
# We passed a template (blueprint) where a final string/message was required, so Pydantic rejected it.Pydantic does validates content step-by-step:
agent=create_agent(model=model, system_prompt="You are a helpful assistant.")
if __name__ == "__main__":
    print("Agent ready. Run: langgraph dev") #if  file is run directly using poetry run filename.py the __name__ == "__main__"  → TRUE and this runs print("Agent ready. Run: langgraph dev"). if file is Imported by something else (like LangGraph) by using poetry langgraph dev in this case, then __name__ == "__main__"  → FALSE and this doesn't run print("Agent ready. Run: langgraph dev")
# response = model.invoke(prompt.format_messages(topic="France"))
#print(prompt.invoke(prompt.format_messages(topic="India"))) # formats the template into a structured message.
# print(model.invoke(prompt.invoke(prompt.format_messages(topic="Python programming")))) # formats the template into a structured message and runs it through the model in one step.
# print(model.invoke(prompt.invoke(prompt.format_messages(topic="Python programming"))).content) # formats the template into a structured message, runs it through the model, and extracts the content from the response. 
#prompt.invoke({...}) → formats the template into a structured message.
# ChatPromptTemplate aren't directly callable like functions. response = model.invoke(prompt(topic="France")) won't work
# response = (prompt | model).invoke({"topic": "Python programming"}) # formats the template and runs it through the model in one step.
# print(response.content)