from django.contrib import admin

from .models import YesNoQuestion, QuestionSet

class YesNoQuestionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in YesNoQuestion._meta.get_fields()]

class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ['description']

admin.site.register(YesNoQuestion, YesNoQuestionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)