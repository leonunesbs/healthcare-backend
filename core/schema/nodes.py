import graphene
from core.models import Colaborator, Evaluation, Patient, Service, Unit
from graphene_django import DjangoObjectType


class ColaboratorNode(DjangoObjectType):
    class Meta:
        model = Colaborator
        filter_fields = []
        interfaces = (graphene.relay.Node, )


class EvaluationNode(DjangoObjectType):
    class Meta:
        model = Evaluation
        filter_fields = []
        interfaces = (graphene.relay.Node,)


class PatientNode(DjangoObjectType):
    class Meta:
        model = Patient
        filter_fields = {
            'full_name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (graphene.relay.Node, )


class ServiceNode(DjangoObjectType):
    class Meta:
        model = Service
        filter_fields = []
        interfaces = (graphene.relay.Node, )


class UnitNode(DjangoObjectType):
    class Meta:
        model = Unit
        filter_fields = []
        interfaces = (graphene.relay.Node, )


class ServiceNode(DjangoObjectType):
    class Meta:
        model = Service
        filter_fields = ['unit']
        interfaces = (graphene.relay.Node, )
