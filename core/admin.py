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
    list_display = [f.name for f in core_models.Evaluation._meta.fields]


@admin.register(core_models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [f.name for f in core_models.Patient._meta.fields] + ['age']

    def age(self, obj):
        return obj.age


@admin.register(core_models.Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(core_models.Service)
class SpecialtyAdmin(admin.ModelAdmin):
    pass


@admin.register(core_models.Unit)
class UnitAdmin(admin.ModelAdmin):
    pass
