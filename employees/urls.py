from django.urls import path

# import views
from .views import login_employee, logout_employee

urlpatterns = [
    path('login', login_employee, name='login-employee'),
    path('logout', logout_employee, name='logout-employee'),
]