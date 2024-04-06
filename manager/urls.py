from django.urls import path

# IMPORT MODULES HERE
from .views import *

urlpatterns = [
    path('', manager_home, name='manager-home'),
]