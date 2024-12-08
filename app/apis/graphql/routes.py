from strawberry.fastapi import GraphQLRouter
from app.apis.graphql.schema import Query
import strawberry

schema = strawberry.Schema(Query)
graphql_router = GraphQLRouter(schema)
