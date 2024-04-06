from django.urls import path

# IMPORT YOUR MODULES HERE
from .view import *

urlpatterns=[
    path('create-member/', create_member),
    path('update-member/<str:pk>', update_member),
    path('delete-member/<str:pk>', delete_member),
    path('check-balance/<str:pk>', check_balance),
    path('member-list/', members_list),
    path('get-member-detail/<str:pk>', get_member_detail),
    path('search_member/', SearchMemberListView.as_view(), name='search-video'),

    # REPORT GENERATION
    path('other-saving-report/<int:check>', generate_other_report),
    path('compulsory-saving-report/<int:check>', generate_compulsory_report),
    path('export-to-other-saving', other_saving_excel, name='export-to-other-saving'),
    path('export-to-compulsory-saving', compulsory_saving_excel, name='export-to-compulsory-saving'),

]