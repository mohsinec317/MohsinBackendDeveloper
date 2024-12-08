import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List
from app.models.database_model import get_db_session
from app.models.trip_model import Trip
from sqlalchemy.orm import Session
from app.apis.graphql.schema import Query

schema = strawberry.Schema(Query)
graphql_router = GraphQLRouter(
    schema,
    context_getter=lambda: {"session": next(get_db_session())}  # Get session from DB session generator
)
