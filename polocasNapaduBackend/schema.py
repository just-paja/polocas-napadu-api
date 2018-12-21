import graphene

import bands.schema

class Query(bands.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
