from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from core.models import Collaborator, Evaluation, Patient, Service, Unit


class TestUnitModel(TestCase):
    def test_unit_model(self):
        unit = Unit.objects.create(name='unit')
        self.assertEqual(unit.name, 'unit')


class TestServiceModel(TestCase):
    def test_service_model(self):
        unit = Unit.objects.create(name='unit')
        service = Service.objects.create(name='service', unit=unit)
        self.assertEqual(service.name, 'service')


class TestCollaboratorModel(TestCase):
    def test_collaborator_model(self):
        user = User.objects.create_user(username='user', password='pass')
        collaborator = Collaborator.objects.create(
            user=user,
            name='name',
            surname='surname',
            email='email@email.com',
            phone='phone',
            role='role'
        )
        self.assertEqual(collaborator.name, 'name')


class TestPatientModel(TestCase):
    def test_patient_model(self):
        patient = Patient.objects.create(
            full_name='full name',
            birth_date=timezone.now()
        )
        self.assertEqual(patient.full_name, 'FULL NAME')


class TestEvaluationModel(TestCase):
    def test_evaluation_model(self):
        evaluation = Evaluation.objects.create(
            patient=Patient.objects.create(
                full_name='full name',
                birth_date=timezone.now()
            ),
            collaborator=Collaborator.objects.create(
                user=User.objects.create_user(
                    username='user', password='pass'),
                name='name',
                surname='surname',
                email='email@email.com',
                phone='phone',
                role='role'
            ),
            service=Service.objects.create(
                name='service',
                unit=Unit.objects.create(name='unit')
            ),
            content='content',
        )
        self.assertEqual(evaluation.content, 'content')
