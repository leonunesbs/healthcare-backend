import core.schema.mutation as core_mutations
import core.schema.query as core_query
import graphene
import graphql_jwt
from core.schema.nodes import UserNode
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType


class Query(core_query.Query, graphene.ObjectType):
    pass


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserNode)

    @classmethod
    def resolve(self, root, info, **kwargs):
        return self(user=info.context.user)


class Mutation(core_mutations.Mutation, graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
