from django.contrib import admin

# Register your models here.
from .models import Student,Ticket
from Student.models import Payment,Tuition,External_Tuition,Attendance
from dashboard.models import Workbook
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    search_fields = ["student_name",]
    list_display = ("student_name","age")
    list_filter = ("student_name",)
    fieldsets = (
        (None,{"fields":("student_name","first_name","last_name","gender","birth_date","grade","parent","subjects","classroom","plan","to_2","to_1","is_external")}),
    )
    @admin.display(description='年齢')
    def age(self, obj):
        return obj.age
    
class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ["student",]
    list_display = ("student","checkin_time" ,"checkout_time")
    list_filter = ("student",)
    fieldsets = (
        (None,{"fields":("student","checkin_time","checkout_time")}),
    )



class TicketAdmin(admin.ModelAdmin):
    search_fields = ["student",]
    list_display = ("student","purchase_date","ticket_type")
    list_filter = ("student","purchase_date",)
    fieldsets = (
        (None,{"fields":("student","remaining_count","usage_count")}),
    )


class TuitionAdmin(admin.ModelAdmin):
    search_fields = ["student"]
    list_display = ("student","amount","due_date","payment_status",)
    list_filter = ("student",)
    fieldsets = (
        (None,{"fields":("student","class_count","payment_status",)}),
    )
        


class External_TuitionAdmin(admin.ModelAdmin):
    search_fields = ["student"]
    list_display = ("student","amount","due_date","payment_status",)
    list_filter = ("student",)
    fieldsets = (
        (None,{"fields":("student","payment_status",)}),
    )

class PaymentAdmin(admin.ModelAdmin):
    search_fields = ["student"]
    list_display = ("student","payment_date","amount","payment_status",)
    list_filter = ("student","payment_date")
    fieldsets = (
        (None,{"fields":("student","payment_date","amount","payment_status",)}),
    )



admin.site.register(Tuition,TuitionAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(External_Tuition,External_TuitionAdmin)
admin.site.register(Attendance,AttendanceAdmin)

