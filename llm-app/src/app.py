from fastapi import FastAPI
from langserve import add_routes

from api import routes
from core.chains import CreateChain


chain = CreateChain().create_chain

app = FastAPI()


app.include_router(routes.router)
add_routes(app, chain, path="/generate_story")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
