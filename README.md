5th file:
poetry add package@latest - install langraph-cli
poetry run langgraph dev - expose as endpoint

1st till 4th file:
poetry run filename.py will use langserve for endpoint creation and endpoint will be hosted on fastapi server.langserve creates endpoint(api) and fastapi is server/container where endpoint exists.langserve adds endpoints (APIs) for our LangChain agent/code automatically.FastAPI creates the server (app)
LangServe registers endpoints inside that server.It attaches endpoints to FastAPI.FastAPI runs the server, and LangServe plugs your LangChain agent into it by automatically creating API endpoints.FastAPI provides the server and routing system where endpoints live.
Backend API (server) → via FastAPI
Agent endpoints → via LangServe
agent is already usable at /langserve_agent_with_tools/invoke