from django.contrib.auth.models import BaseUserManager

class EmployeeManager(BaseUserManager):
    def _create_user(self, employee_id, password=None, **extra_fields):
        print(employee_id)
        if not employee_id:
            raise ValueError('Employee Id Is Required')

        user = self.model(employee_id=employee_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user  

    def create_user(self, employee_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', False)

        return self._create_user(employee_id=employee_id, password=password, **extra_fields)
    
    def create_superuser(self, employee_id, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('is_active', True)
        extra.setdefault('is_admin', True)

        return self._create_user(employee_id=employee_id, password=password, **extra)
        
         

