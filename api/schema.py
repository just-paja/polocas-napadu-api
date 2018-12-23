import graphene

import bands.schema
import locations.schema
import profiles.schema
import shows.schema


class Query(
    bands.schema.Query,
    locations.schema.Query,
    profiles.schema.Query,
    shows.schema.Query,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
