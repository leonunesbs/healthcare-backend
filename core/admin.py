from django.contrib import admin

import core.models as core_models


@admin.register(core_models.EvaluationAttachment)
class EvaluationAttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(core_models.Colaborator)
class ColaboratorAdmin(admin.ModelAdmin):
    pass


@admin.register(core_models.Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    pass


@admin.register(core_models.Patient)
class PatientAdmin(admin.ModelAdmin):
    pass


@admin.register(core_models.Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(core_models.Service)
class SpecialtyAdmin(admin.ModelAdmin):
    pass


@admin.register(core_models.Unit)
class UnitAdmin(admin.ModelAdmin):
    pass
