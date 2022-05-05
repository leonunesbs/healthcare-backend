import graphene
from core.models import Evaluation, Patient, Service, Unit
from core.schema.nodes import (EvaluationNode, PatientNode, ServiceNode,
                               UnitNode)
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from graphql import GraphQLError
from graphql_relay import from_global_id


class CreatePatient(graphene.Mutation):
    class Arguments:
        full_name = graphene.String(required=True)
        birth_date = graphene.DateTime(required=True)
        cpf = graphene.String()
        email = graphene.String()
        phone = graphene.String()

    created = graphene.Boolean()
    patient = graphene.Field(PatientNode)

    @classmethod
    def mutate(cls, root, info, full_name, birth_date, cpf=None, email=None, phone=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError(
                _('You must be logged in to perform this action'))
        patient, created = Patient.objects.get_or_create(
            full_name=full_name.strip().upper(),
            birth_date=birth_date,
            cpf=cpf,
            email=email.strip(),
            phone=phone.strip()
        )

        return CreatePatient(created=created, patient=patient)


class DeletePatient(graphene.Mutation):
    class Arguments:
        patient_id = graphene.ID(required=True)

    deleted = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, patient_id):
        if not info.context.user.is_authenticated:
            raise GraphQLError(
                _('You must be logged in to perform this action'))
        patient_id = from_global_id(patient_id)[1]
        patient = Patient.objects.get(id=patient_id)
        patient.delete()
        return DeletePatient(deleted=True)


class UpdatePatient(graphene.Mutation):
    class Arguments:
        patient_id = graphene.ID(required=True)
        full_name = graphene.String()
        birth_date = graphene.DateTime()
        cpf = graphene.String()
        email = graphene.String()
        phone = graphene.String()

    updated = graphene.Boolean()
    patient = graphene.Field(PatientNode)

    @classmethod
    def mutate(cls, root, info, patient_id, full_name=None,  birth_date=None, cpf=None, email=None, phone=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError(
                _('You must be logged in to perform this action'))
        try:
            patient = Patient.objects.get(pk=from_global_id(patient_id)[1])
        except Patient.DoesNotExist:
            raise GraphQLError(_('Patient does not exist'))

        if full_name is not None:
            patient.full_name = full_name.strip().upper()
        if birth_date is not None:
            patient.birth_date = birth_date
        if cpf is not None:
            patient.cpf = cpf.strip()
        if email is not None:
            patient.email = email.strip().lower()
        if phone is not None:
            patient.phone = phone.strip()

        patient.save()

        return UpdatePatient(updated=True, patient=patient)


class CreateEvaluation(graphene.Mutation):
    class Arguments:
        patient_id = graphene.ID(required=True)
        service_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    created = graphene.Boolean()
    evaluation = graphene.Field(EvaluationNode)

    @classmethod
    def mutate(cls, root, info, patient_id, service_id, content):
        if info.context.user.is_authenticated is False:
            raise GraphQLError(
                _('You must be logged in to perform this action'))
        try:
            patient = Patient.objects.get(id=from_global_id(patient_id)[1])
            service = Service.objects.get(id=from_global_id(service_id)[1])
        except Patient.DoesNotExist:
            raise GraphQLError(_('Patient does not exist'))
        except Service.DoesNotExist:
            raise GraphQLError(_('Service does not exist'))

        evaluation, created = Evaluation.objects.get_or_create(
            collaborator=info.context.user.collaborator,
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
        if info.context.user.is_authenticated is False:
            raise GraphQLError(
                _('You must be logged in to perform this action'))
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
        if info.context.user.is_authenticated is False:
            raise GraphQLError(
                _('You must be logged in to perform this action'))

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
        if info.context.user.is_authenticated is False:
            raise GraphQLError(
                _('You must be logged in to perform this action'))
        try:
            unit = Unit.objects.get(id=from_global_id(unit_id)[1])
        except Unit.DoesNotExist:
            raise GraphQLError(_('Unit does not exist'))

        service, created = Service.objects.get_or_create(
            unit=unit,
            name=name
        )

        return CreateService(created=created, service=service)


class AddServiceCollaborator(graphene.Mutation):
    class Arguments:
        service_id = graphene.ID(required=True)
        collaborator_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    service = graphene.Field(ServiceNode)

    @classmethod
    def mutate(cls, root, info, service_id, collaborator_id):
        if info.context.user.is_authenticated is False:
            raise GraphQLError(
                _('You must be logged in to perform this action'))

        try:
            service = Service.objects.get(id=from_global_id(service_id)[1])
        except Service.DoesNotExist:
            raise GraphQLError(_('Service does not exist'))

        try:
            collaborator = Patient.objects.get(
                id=from_global_id(collaborator_id)[1])
        except Patient.DoesNotExist:
            raise GraphQLError(_('Patient does not exist'))

        service.collaborators.add(collaborator)
        service.collaborators.save()

        ok = True

        return AddServiceCollaborator(ok=ok, service=service)


class Mutation(graphene.ObjectType):
    create_patient = CreatePatient.Field()
    delete_patient = DeletePatient.Field()
    update_patient = UpdatePatient.Field()
    create_evaluation = CreateEvaluation.Field()
    update_evaluation = UpdateEvaluation.Field()

    create_unit = CreateUnit.Field()

    create_service = CreateService.Field()
    add_service_collaborator = AddServiceCollaborator.Field()
