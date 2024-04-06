from django.urls import path

from .views import *

urlpatterns = [
    path('', credit_list, name='credit-class-home'),
    path('credit-info/<str:pk>', credit_info, name='credit-class-info'),
    path('credit-susspesnion', susspend_member),
]