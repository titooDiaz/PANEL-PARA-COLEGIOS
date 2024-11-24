from django.contrib import admin
from .models import ScheduleParts, Grade, Subjects, DailySchedule


class SchedulePartsProxy(ScheduleParts):
    class Meta:
        proxy = True
        verbose_name_plural = 'Fraccion de horarios'

class SubjectsProxy(Subjects):
    class Meta:
        proxy = True
        verbose_name_plural = 'Subjects Escolares'

class GradeProxy(Grade):
    class Meta:
        proxy = True
        verbose_name_plural = 'Grades Escolares'

class DailyScheduleProxy(DailySchedule):
    class Meta:
        proxy = True
        verbose_name_plural = 'Horarios Escolares'

admin.site.register(DailyScheduleProxy)
admin.site.register(SchedulePartsProxy)
admin.site.register(GradeProxy)
admin.site.register(SubjectsProxy)