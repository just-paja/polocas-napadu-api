import graphene

import bands.schema
import locations.schema

class Query(bands.schema.Query, locations.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
