import graphene
from core.models import Evaluation, Patient, Service, Unit
from core.schema.nodes import (EvaluationNode, PatientNode, ServiceNode,
                               UnitNode)
from django.utils.translation import gettext as _
from graphql import GraphQLError
from graphql_relay import from_global_id


class CreatePatient(graphene.Mutation):
    class Arguments:
        full_name = graphene.String(required=True)
        birth_date = graphene.DateTime(required=True)
        email = graphene.String()
        phone = graphene.String()

    created = graphene.Boolean()
    patient = graphene.Field(PatientNode)

    @classmethod
    def mutate(cls, root, info, full_name, birth_date, email=None, phone=None):
        patient, created = Patient.objects.get_or_create(
            full_name=full_name,
            birth_date=birth_date,
            email=email,
            phone=phone
        )

        return CreatePatient(created=created, patient=patient)


class CreateEvaluation(graphene.Mutation):
    class Arguments:
        patient_id = graphene.ID(required=True)
        service_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    created = graphene.Boolean()
    evaluation = graphene.Field(EvaluationNode)

    @classmethod
    def mutate(cls, root, info, patient_id, service_id, content):
        try:
            patient = Patient.objects.get(id=from_global_id(patient_id)[1])
            service = Service.objects.get(id=from_global_id(service_id)[1])
        except Patient.DoesNotExist:
            raise GraphQLError(_('Patient does not exist'))
        except Service.DoesNotExist:
            raise GraphQLError(_('Service does not exist'))

        evaluation, created = Evaluation.objects.get_or_create(
            colaborator=info.context.user.colaborator,
            patient=patient,
            service=service,
            content=content
        )

        return CreateEvaluation(created=created, evaluation=evaluation)


class UpdateEvaluation(graphene.Mutation):
    class Arguments:
        evaluation_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    ok = graphene.Boolean()
    evaluation = graphene.Field(EvaluationNode)

    @classmethod
    def mutate(cls, root, info, evaluation_id, content):
        evaluation = Evaluation.objects.get(
            id=from_global_id(evaluation_id)[1])
        evaluation.content = content
        evaluation.save()

        ok = True

        return UpdateEvaluation(ok=ok, evaluation=evaluation)


class CreateUnit(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    created = graphene.Boolean()
    unit = graphene.Field(UnitNode)

    @classmethod
    def mutate(cls, root, info, name):
        unit, created = Unit.objects.get_or_create(
            name=name
        )

        return CreateUnit(created=created, unit=unit)


class CreateService(graphene.Mutation):
    class Arguments:
        unit_id = graphene.ID(required=True)
        name = graphene.String(required=True)

    created = graphene.Boolean()
    service = graphene.Field(ServiceNode)

    @classmethod
    def mutate(cls, root, info, unit_id, name):
        try:
            unit = Unit.objects.get(id=from_global_id(unit_id)[1])
        except Unit.DoesNotExist:
            raise GraphQLError(_('Unit does not exist'))

        service, created = Service.objects.get_or_create(
            unit=unit,
            name=name
        )

        return CreateService(created=created, service=service)


class AddServiceColaborator(graphene.Mutation):
    class Arguments:
        service_id = graphene.ID(required=True)
        colaborator_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    service = graphene.Field(ServiceNode)

    @classmethod
    def mutate(cls, root, info, service_id, colaborator_id):
        try:
            service = Service.objects.get(id=from_global_id(service_id)[1])
        except Service.DoesNotExist:
            raise GraphQLError(_('Service does not exist'))

        try:
            colaborator = Patient.objects.get(
                id=from_global_id(colaborator_id)[1])
        except Patient.DoesNotExist:
            raise GraphQLError(_('Patient does not exist'))

        service.colaborators.add(colaborator)
        service.colaborators.save()

        ok = True

        return AddServiceColaborator(ok=ok, service=service)


class Mutation(graphene.ObjectType):
    create_patient = CreatePatient.Field()
    create_evaluation = CreateEvaluation.Field()
    update_evaluation = UpdateEvaluation.Field()

    create_unit = CreateUnit.Field()

    create_service = CreateService.Field()
    add_service_colaborator = AddServiceColaborator.Field()
