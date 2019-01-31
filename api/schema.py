import graphene

import bands.schema
import games.schema
import inspirations.schema
import locations.schema
import profiles.schema
import shows.schema
import theatre_sports.schema


class PublicQuery(
    bands.schema.Query,
    games.schema.Query,
    inspirations.schema.Query,
    locations.schema.Query,
    profiles.schema.Query,
    shows.schema.Query,
    theatre_sports.schema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    theatre_sports.schema.Mutations,
    graphene.ObjectType
):
    pass

PUBLIC = graphene.Schema(query=PublicQuery, mutation=Mutation)
