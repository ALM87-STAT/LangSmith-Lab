from fastapi import FastAPI
from langserve import add_routes

from src.api import routes
from src.core.chains import CreateChain


chain = CreateChain().create_chain

app = FastAPI()


app.include_router(routes.router)
add_routes(app, chain, path="/generate_story")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
