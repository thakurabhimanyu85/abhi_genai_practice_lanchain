from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

model=init_chat_model(model="llama-3.1-8b-instant",model_provider="groq",  temperature=0.7)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "What is the capital of {country}?"),
    ]
)
# response = model.invoke(prompt.format_messages(country="France"))
#print(prompt.invoke(prompt.format_messages(country="India"))) # formats the template into a structured message.
print(model.invoke(prompt.invoke(prompt.format_messages(country="India")))) # formats the template into a structured message and runs it through the model in one step.
print(model.invoke(prompt.invoke(prompt.format_messages(country="India"))).content) # formats the template into a structured message, runs it through the model, and extracts the content from the response. 
#prompt.invoke({...}) → formats the template into a structured message.
# ChatPromptTemplate aren't directly callable like functions. response = model.invoke(prompt(country="France")) won't work
response = (prompt | model).invoke({"country": "France"}) # formats the template and runs it through the model in one step.
print(response.content)