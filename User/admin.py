from django.contrib import admin
from Student.models import Tuition,Payment
# Register your models here.
from .models import User

class CustomerAdmin(admin.ModelAdmin):
    search_fields = ["username"]
    list_display = ("username","customer_id","email","parent_tel",)
    list_filter = ("username",)
    fieldsets = (
        (None,{"fields":("customer_id","username","parent_first_name","parent_last_name","parent_tel","email","is_superuser","date_joined","is_teacher","password")}),
    )


admin.site.register(User,CustomerAdmin)
