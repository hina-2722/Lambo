from django.contrib import admin
from .models import Reservation,Report
# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
    list_display = ("student",'reserved_time',"time","schedule", )
    list_filter = ('reserved_time',"schedule",)
    fieldsets = (
        (None,{"fields":("student","schedule","reserved_time","time")}),
    )

class ReportAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'reserved_date', 'time_slot', 'instructor_name', 'comment')
    list_filter = ('reservation', 'comment')
    fieldsets = (
        (None, {'fields': ('reservation','goal','comment')}),
    )


    def reserved_date(self, obj):
        return obj.reservation.reserved_time

    def time_slot(self, obj):
        return obj.reservation.time

    def instructor_name(self, obj):
        return obj.reservation.schedule.instructor_name



admin.site.register(Reservation,ReservationAdmin)

admin.site.register(Report,ReportAdmin)