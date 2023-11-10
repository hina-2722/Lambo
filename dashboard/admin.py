from django.contrib import admin
from .models import TeacherEvaluation,Workbook

class QuestionnaireAdmin(admin.ModelAdmin):
    search_fields = ["instructor",]
    list_display = ("instructor","instructor_rating","curriculum_rating","satisfaction_rating","student")
    list_filter = ("instructor",)
    fieldsets = (
        (None,{"fields":("instructor","student")}),
    )

class WorkbookAdmin(admin.ModelAdmin):
    search_fields = ["student",]
    list_display = ("name","price","level","student")
    list_filter = ("student",)
    fieldsets = (
        (None,{"fields":("name","image","price","purchase_link","level","student")}),
    )

admin.site.register(TeacherEvaluation,QuestionnaireAdmin)
admin.site.register(Workbook,WorkbookAdmin)