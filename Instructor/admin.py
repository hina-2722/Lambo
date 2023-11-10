from django.contrib import admin

# Register your models here.
from .models import Instructor,Schedule,TimeSlot,Salary,MonthlySalary
from User.models import User

class InstructorAdmin(admin.ModelAdmin):
    search_fields = ["name",]
    list_display = ("name","gender","birth_date","sarary","like")
    list_filter = ("name",)
    fieldsets = (
        (None,{"fields":("name","is_teacher","photo","birth_date","gender","sarary","like","online_support","in_person_support")}),
    )

class ReportAdmin(admin.ModelAdmin):
    search_fields = ["date",]
    list_display = ("date","instructor",)
    list_filter = ("date",)
    fieldsets = (
        (None,{"fields":("date","instructor","content",)}),
    )

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('instructor_name', 'date', 'display_time_slots')
    list_filter = ('instructor_name', 'date', 'time')
    fieldsets = (
        (None,{"fields":('instructor_name',"date","time")}),
    )

    def display_time_slots(self, obj):
        return ", ".join(str(time) for time in obj.time.all())

    display_time_slots.short_description = 'Time Slots'

class TimeslotAdmin(admin.ModelAdmin):
    list_display = ('time',)
    list_filter = ('time',)
    fieldsets = (
        (None,{"fields":('time',)}),
    )

class SalaryAdmin(admin.ModelAdmin):
    list_display = ('instructor',)
    list_filter = ('instructor',)
    fieldsets = (
        (None,{"fields":('instructor',"monthly_salaries","annual_salaries")}),
    )
class MonthlySalaryAdmin(admin.ModelAdmin):
    list_display = ('month',"koma","amount",)
    list_filter = ('month',"koma","amount",)
    fieldsets = (
        (None,{"fields":('month',"koma","amount",)}),
    )


admin.site.register(Instructor,InstructorAdmin)
admin.site.register(Schedule,ScheduleAdmin)
admin.site.register(TimeSlot,TimeslotAdmin)
admin.site.register(Salary,SalaryAdmin)
admin.site.register(MonthlySalary,MonthlySalaryAdmin)