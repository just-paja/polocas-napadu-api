import graphene

import bands.schema
import locations.schema
import shows.schema

class Query(
    bands.schema.Query,
    locations.schema.Query,
    shows.schema.Query,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query)
