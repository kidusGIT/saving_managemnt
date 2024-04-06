from rest_framework.serializers import ModelSerializer

# IMPORT MODELS HERE
from members.models import Member
from . import models

# MEMBER SERILIZER
class MemberSerilizer(ModelSerializer):
    class Meta:
        model = Member
        fields = ['member_id', 'first_name', 'father_name', 'garnd_father_name',
                  'city', 'sub_city', 'woreda', 'house_num', 'email', 'phone_num', 'save_count', 'age', 'created_date']

# SAVING SERILIZER
class  SavingTypeSerilizer(ModelSerializer):
    class Meta:
        model = models.SavingType
        fields = ['id', 'account_name']

        
class SavingAccountSerilizer(ModelSerializer):
    saving_type = SavingTypeSerilizer()
    member = MemberSerilizer()

    class Meta:
        model = models.SavingAccount
        fields = ['account_id', 'member', 'saving_type', 'balance', 'is_suspended',
            'is_active', 'created_date']


class SavingTransactionSerilizer(ModelSerializer):
    # account = SavingAccountSerilizer(many=True)   
    account = SavingAccountSerilizer()  
    class Meta:
        model = models.SavingTransaction
        fields = ['id', 'account', 'balance', 'withdraw', 'deposit', 'interest', 'created_date']

# COMPULSORY SAVING
class CompulsorySavingSerilizer(ModelSerializer):
    member = MemberSerilizer()
    class Meta:
        model = models.CompulsorySaving
        fields = ['account_id', 'member', 'balance', 'is_suspended', 'created_date']


class CompulsoryTransactionSerilizer(ModelSerializer):
    account = CompulsorySavingSerilizer()
    class Meta:
        model = models.CompulsoryTransaction
        fields = ['id', 'account', 'balance', 'withdraw', 'deposit', 'interest', 'created_date']
