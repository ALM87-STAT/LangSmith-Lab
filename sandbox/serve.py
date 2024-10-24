#!/usr/bin/env python
"""Example LangChain server exposes multiple runnables (LLMs in this case)."""

from fastapi import FastAPI
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai.model_garden import ChatAnthropicVertex
from langchain_openai import ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)

add_routes(
    app,
    ChatOpenAI(model="gpt-4o-mini"),
    path="/openai",
)

add_routes(
    app,
    ChatVertexAI(model="gemini-1.0-pro-002", temperature=0.5),
    path="/google-vertexai",
)

add_routes(
    app,
    ChatAnthropicVertex(
        model_name="claude-3-5-sonnet@20240620", location="europe-west1"
    ),
    path="/anthropic",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("serve:app", host="localhost", port=8000, reload=True)
