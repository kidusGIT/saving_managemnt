from django.urls import path

# IMPORT USER BUILT MODULE HERE
from .views import get_members_transaction, compulsory_monthly_saving, generate_report

urlpatterns =[ 
    # MEMBER'S TRANSACTION
    path('member-transction/<str:pk>', get_members_transaction, name='member-transction'),
    path('member-transction-report/<str:pk>/<int:check>', generate_report, name='member-transction-report'),

    # MONTHLY SAVINGS
    path('monthly-savings', compulsory_monthly_saving, name='monthly-savings'),
]

