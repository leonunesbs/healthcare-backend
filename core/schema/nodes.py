import graphene
from core.models import Colaborator, Evaluation, Patient, Service, Unit
from django.utils.translation import gettext as _
from graphene_django import DjangoObjectType


class ColaboratorNode(DjangoObjectType):
    full_name = graphene.String()

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
    age = graphene.String()
    latest_evaluation = graphene.DateTime(source='get_latest_evaluation_date')

    class Meta:
        model = Patient
        filter_fields = {
            'full_name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (graphene.relay.Node, )

    def resolve_age(self, info):
        if self.age == 0:
            if self.age_in_months == 0:
                if self.age_in_days == 1:
                    return f'{self.age_in_days} {_("day")}'
                else:
                    return f'{self.age_in_days} {_("days")}'
            elif self.age_in_months == 1:
                return f'{self.age_in_months} {_("month")}'
            else:
                return f'{self.age_in_months} {_("months")}'

        return f'{self.age} {_("years")}'


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
