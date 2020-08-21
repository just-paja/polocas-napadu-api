import graphene
import graphql_jwt

import accounting.schema # noqa
import bands.schema
import blog.schema
import games.schema
import inspirations.schema
import locations.schema
import profiles.schema
import shows.schema
import theatre_sports.schema
import tickets.schema
import voting.schema


class PublicQuery(
    bands.schema.Query,
    blog.schema.Query,
    games.schema.Query,
    inspirations.schema.Query,
    locations.schema.Query,
    profiles.schema.Query,
    shows.schema.Query,
    theatre_sports.schema.Query,
    tickets.schema.Query,
    voting.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    theatre_sports.schema.Mutations,
    shows.schema.Mutations,
    voting.schema.Mutations,
    graphene.ObjectType,
):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


PUBLIC = graphene.Schema(query=PublicQuery, mutation=Mutation)
