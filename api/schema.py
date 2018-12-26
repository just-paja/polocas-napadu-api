import graphene

import bands.schema
import locations.schema
import profiles.schema
import shows.schema


class PublicQuery(
    bands.schema.Query,
    locations.schema.Query,
    profiles.schema.Query,
    shows.schema.Query,
    graphene.ObjectType
):
    pass


PUBLIC = graphene.Schema(query=PublicQuery)
