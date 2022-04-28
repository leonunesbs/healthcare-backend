from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _


class Unit(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
        help_text=_('unit name'),
    )

    class Meta:
        verbose_name = _('unit')
        verbose_name_plural = _('units')

    def __str__(self):
        return self.name


class Service(models.Model):
    unit = models.ForeignKey(
        'core.Unit',
        on_delete=models.CASCADE,
        verbose_name=_('unit'),
        help_text=_('unit'),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
        help_text=_('service name'),
    )
    colaborators = models.ManyToManyField(
        'core.Colaborator',
        verbose_name=_('colaborators'),
        help_text=_('colaborators'),
        related_name='services',
        blank=True,
    )

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')

    def __str__(self):
        return self.name


class Colaborator(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_('name'))
    surname = models.CharField(max_length=255, verbose_name=_('surname'))
    email = models.EmailField(verbose_name=_('email'))
    phone = models.CharField(max_length=255, verbose_name=_('phone'))
    role = models.CharField(max_length=255, verbose_name=_('role'))

    class Meta:
        verbose_name = _('colaborator')
        verbose_name_plural = _('colaborators')

    def __str__(self):
        return self.name

    @property
    def full_name(self):
        return f'{self.name} {self.surname}'

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

    def save(self, *args, **kwargs):
        self.clean_fields()
        super().save(*args, **kwargs)


class Patient(models.Model):
    full_name = models.CharField(max_length=100, verbose_name=_('full name'))
    birth_date = models.DateField(verbose_name=_('birth date'))
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True,
                             null=True, verbose_name=_('phone'))
    cpf = models.CharField(max_length=20, blank=True,
                           null=True, verbose_name=_('CPF'))

    class Meta:
        verbose_name = _('patient')
        verbose_name_plural = _('patients')

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        today = timezone.now()
        return today.year - self.birth_date.year - \
            ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

    def save(self, *args, **kwargs):
        self.clean_fields()
        super().save(*args, **kwargs)


class EvaluationAttachment(models.Model):
    evaluation = models.ForeignKey('core.Evaluation', on_delete=models.CASCADE, verbose_name=_(
        'evaluation'), related_name='attachments')
    file = models.FileField(upload_to='evaluations/attachments/')

    class Meta:
        verbose_name = _('evaluation attachment')
        verbose_name_plural = _('evaluation attachments')

    def __str__(self):
        return self.file.name


class Evaluation(models.Model):
    service = models.ForeignKey('core.Service', on_delete=models.CASCADE, verbose_name=_(
        'service'), related_name='evaluations')
    patient = models.ForeignKey(
        'core.Patient', on_delete=models.CASCADE, related_name='evaluations', verbose_name=_('patient'))
    colaborator = models.ForeignKey(
        'core.Colaborator', on_delete=models.CASCADE, related_name='evaluations', verbose_name=_('colaborator'))
    content = models.TextField(verbose_name=_('content'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('evaluation')
        verbose_name_plural = _('evaluations')

    def __str__(self):
        return str(self.patient)


class Prescription(models.Model):
    service = models.ForeignKey('core.Service', on_delete=models.CASCADE, verbose_name=_(
        'prescription'), related_name='prescriptions')
    patient = models.ForeignKey(
        'core.Patient',
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name=_('patient'),
    )
    colaborator = models.ForeignKey(
        'core.Colaborator',
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name=_('colaborator'),
    )
    content = models.TextField(verbose_name=_('content'))
    prescription_date = models.DateField(
        verbose_name=_('prescription date'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))

    class Meta:
        verbose_name = _('prescription')
        verbose_name_plural = _('prescriptions')

    def __str__(self):
        return str(self.patient)
