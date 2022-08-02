from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('username', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# class PatientAdmin(admin.ModelAdmin):
#     list_display = ('doctor_id', 'name', 'age', 'weight', 'gender')
#     search_fields = ('doctor_id', 'name')
#
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(PatientDetails, PatientAdmin)