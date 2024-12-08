from fastapi import FastAPI
from app.apis.database_routes import router as database_router
from app.apis.rest_routes import rest_router
from app.apis.graphql_routes import graphql_router

app = FastAPI()

app.include_router(database_router, prefix="/api", tags=["Database"])
app.include_router(rest_router, prefix="/api", tags=["RESTful"])
app.include_router(graphql_router, prefix="/graphql", tags=["graphql"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
