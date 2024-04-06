from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# import user builte module here
from .models import Employee
from .forms import EmployeeChangeForm, EmployeeCreationForm

# @admin.register(Employee)
class CustomEmployeeAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    form = EmployeeChangeForm
    model = Employee

    list_display = ['employee_id', 'full_name', 'email', 'is_admin']
    list_filter = ['is_admin']
    fieldsets = [
        [None, {'fields' : [
            'employee_id', 'full_name', 'phone_no', 'city', 'sub_city',
            'woreda', 'house_no', 'email', 'is_manager', 'is_accountant',
            'is_credit_class', 'is_saving_super', 
        
        ]}],
        ['Permissions', {'fields':['is_admin', 'is_active']}],
    ]

    add_fieldsets = [
        [None, {
            'classes': ['wide', ],
            'fields': ['employee_id', 'password1', 'password2',
                'full_name', 'phone_no', 'city', 'sub_city',
                'woreda', 'house_no', 'email', 'is_manager', 'is_accountant',
                'is_credit_class', 'is_saving_super',       
            ],
        }],
    ]

    search_fields= ['employee_id', 'full_name']
    ordering = ('employee_id',)
    filter_horizontal = ()

admin.site.register(Employee, CustomEmployeeAdmin)

