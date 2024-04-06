from django.urls import path

# IMPORT USER BUILT MODULE HERE
from . import views

urlpatterns =[ 
    # MONTHLY SAVINGS
    path('member-savings', views.members_savings),
    path('change-save-account', views.change_save_counts),
    path('check-has-saved', views.check_has_saved),
    path('members-that-do-not-save/<int:amount>', views.members_that_do_not_save),
    path('set-time', views.set_time),
    path('get-time', views.get_time),

    # DISPLAYE MONTHLY SAVINGS
    path('supervisor-home', views.index_page, name='supervisor-home'),
    path('monthly-savings', views.compulsory_monthly_saving, name='monthly-savings'),
    path('members-lists', views.members_list, name='members-lists'),

    # EMAIL SENDING
    path('send-email', views.send_email_to_member),

]

