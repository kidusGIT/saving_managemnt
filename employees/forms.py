from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# import user built modules here
from .models import Employee

class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'full_name']

class EmployeeChangeForm(UserChangeForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'full_name']