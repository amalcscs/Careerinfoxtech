from django.contrib import admin
from . models import *
admin.site.register(candidates)
admin.site.register(designation)
admin.site.register(question)
admin.site.register(login)

# Register your models here.
class exam_timing_main(admin.ModelAdmin):
    list_display = ('from_date_time', 'to_date_time')
admin.site.register(exam_timing, exam_timing_main)