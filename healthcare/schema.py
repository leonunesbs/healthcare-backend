import core.schema.mutation as core_mutations
import core.schema.query as core_query
import graphene
import graphql_jwt


class Query(core_query.Query, graphene.ObjectType):
    pass


class Mutation(core_mutations.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
