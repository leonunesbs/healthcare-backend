import graphene
from core.models import Patient, Service, Unit
from core.schema.nodes import PatientNode, ServiceNode, UnitNode
from django.utils.translation import gettext as _
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_relay import from_global_id


class Query(graphene.ObjectType):
    patient = graphene.Field(PatientNode, id=graphene.ID())

    all_patients = DjangoFilterConnectionField(PatientNode)
    all_services = DjangoFilterConnectionField(ServiceNode)
    all_units = DjangoFilterConnectionField(UnitNode)

    def resolve_patient(self, info, id, **kwargs):
        try:
            return Patient.objects.get(pk=from_global_id(id)[1])
        except Patient.DoesNotExist:
            raise GraphQLError(_('Patient does not exist'))

    def resolve_all_patients(self, info, **kwargs):
        # if not info.context.user.is_authenticated:
        #     raise GraphQLError(_('You are not allowed to access this data'))

        return Patient.objects.all()

    def resolve_all_services(self, info, **kwargs):
        if not info.context.user.is_staff:
            raise GraphQLError(_('You are not allowed to access this data'))

        return Service.objects.all()

    def resolve_all_units(self, info, **kwargs):
        if not info.context.user.is_staff:
            raise GraphQLError(_('You are not allowed to access this data'))

        return Unit.objects.all()
