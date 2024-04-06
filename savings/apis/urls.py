from django.urls import path

# IMPORT USER BUILT MODULE HERE
from . import views 

urlpatterns =[ 
    # CRETAE ACCOUNT
    path('create-account/<str:pk>', views.create_account), #
    path('create-saving-account/<int:pk>', views.create_saving_account), #
    path('compulsory-detail/<str:pk>', views.get_compulsory_detial), #
    path('saving-account-detail/<int:pk>', views.get_detail_saving_account), #

    # SIWCTH AND CHANGE ACCOUNT
    path('change-saving-account/<int:account>/<str:active>', views.change_account), # 
    path('update-account/<str:pk>/<str:active>', views.update_account), #

    # DIPOSIT AND WITHDRAW
    path('deposit-to-compulosry/<int:pk>/<int:id>', views.deposit_to_compulsory), #
    path('withdraw-to-compulosry/<int:pk>', views.withdraw_from_compulsory), #

    path('deposite-to-saving/<int:pk>', views.deposite_to_savings),
    path('withdraw-to-saving/<int:pk>', views.withdraw_to_savings),

    # SAING ACCOUNT TYPE
    path('account-type', views.get_account_type),

    # MEMBER SAVINGS
    path('member-savings/<str:pk>', views.get_member_savings),

    # MONTHLY SAVINGS
    path('member-savings', views.members_savings),
    path('change-save-account', views.change_save_counts),
    path('check-has-saved', views.check_has_saved),

    # GET ID
    path('get-id', views.get_member_id),

]

