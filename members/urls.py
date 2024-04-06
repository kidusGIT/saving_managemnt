from django.urls import path

# IMPORT YOUR MODULES HERE
from .views import member_list, create_member, update_member, delete_member, export_xls, account_report

urlpatterns =[
    path('', member_list, name='member-list'),
    path('create-member', create_member, name='create-member'),
    path('memeber-info/<str:pk>', update_member, name='memeber-info'),
    path('delete-member/<str:pk>', delete_member, name='delete-member'),
    path('accountant-report', account_report, name='accountant-report'),

    # GENERATE REPORT
    path('generate-report', export_xls, name='generate-report'),
]

