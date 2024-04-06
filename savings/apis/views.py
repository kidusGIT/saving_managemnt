from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

# IMPORT USER BUILT MODULE HERE
from members.models import Member
from savings.models import CompulsorySaving, CompulsoryTransaction, SavingAccount, SavingType, SavingTransaction
from . import serilizers
from savings.helpers import *
# ACCOUNT LIST

# CREATE COMPULSORY ACCOUNT
@api_view(['POST'])
@login_required
def create_account(request, pk):
    member = Member.objects.get(member_id=pk)
    data = request.data
    
    saving = CompulsorySaving()

    saving.account_id = data['account_id']
    saving.balance = data['balance']
    saving.member = member    
        
    saving.save()
    id = data['account_id']
    balance = data['balance']
    
    compulsory = CompulsorySaving.objects.get(account_id=id)
    transaction = CompulsoryTransaction()
    transaction.deposit = data['balance']
    transaction.account = compulsory 
    transaction.balance = balance
    transaction.save()

    member.has_saved = True
    member.save()

    compulsory_vault_deposit(float(balance))

    return Response('inserted')

# CREATE SAVING ACCOUNT
@api_view(['POST'])
@login_required
def create_saving_account(request, pk):
    member = Member.objects.get(member_id=pk)

    data = request.data
    saving_type = SavingType.objects.get(id=data['saving_type'])

    saving_account = SavingAccount()
    saving_account.account_id = data['account_id']
    saving_account.saving_type = saving_type
    saving_account.balance = data['balance']
    saving_account.member = member
    saving_account.is_active = True

    saving_account.save()

    transaction = SavingTransaction()
    transaction.account = SavingAccount.objects.get(account_id=data['account_id'])
    transaction.deposit = data['balance']
    transaction.balance = data['balance']
    transaction.save()
    balance = data['balance']

    saving_vault_deposit(float(balance))

    return Response('inseted')

# UPDATE ACCOUNT
@api_view(['POST'])
@login_required
def update_account(request, pk, active):
    member = Member.objects.get(member_id=pk)
    balance = change_transaction(active)
    if balance == -1:
        return Response(status=400, data='Account is suspended')

    else:
        data = request.data.copy()
        saving_type = SavingType.objects.get(id=data['saving_type'])

        saving_account = SavingAccount()
        saving_account.account_id = data['account_id']
        saving_account.saving_type = saving_type
        saving_account.balance = balance
        saving_account.member = member
        saving_account.is_active = True
        saving_account.save()        
        
        account = SavingAccount.objects.get(account_id=data['account_id'])
        transaction = SavingTransaction()
        transaction.account = account
        transaction.deposit = balance
        transaction.balance = balance
        transaction.save()       

        return Response(status=200, data='created')

# CHANGE ACCOUNT
@api_view(['GET'])
@login_required
def change_account(request, account, active):
    balance = change_transaction(active)
    
    # check account suspension
    if balance == -1:
        return Response(status=400, data='Account is suspended')
    
    else:
        new_account = SavingAccount.objects.filter(account_id=account).select_related('saving_type').select_related('member').get()
        new_account.balance = balance
        new_account.is_active = True
        new_account.save()

        saving_account = SavingAccount.objects.get(account_id=account)
        transaction = SavingTransaction()
        transaction.account = saving_account
        transaction.deposit = balance
        transaction.balance = balance
        transaction.save()

        return Response(status=200, data='changed')

# GET COMPULSORY DETAIL
@api_view(['GET'])
@login_required
def get_compulsory_detial(request, pk):
    try:
        compulsory = CompulsorySaving.objects.filter(member=pk).select_related('member').get()
    except:
        return Response('No Data Found')
    
    serilizer = serilizers.CompulsorySavingSerilizer(compulsory, many=False)
    return Response(serilizer.data)

@api_view(['GET'])
@login_required
def get_member_savings(request, pk):
    saving = SavingAccount.objects.filter(member=pk).select_related('saving_type').select_related('member')

    serilizer = serilizers.SavingAccountSerilizer(saving, many=True)
    return Response(serilizer.data)

@api_view(['GET'])
@login_required
def get_account_type(request):
    accounts = SavingType.objects.all()

    serilizer = serilizers.SavingTypeSerilizer(accounts, many=True)
    return Response(serilizer.data)


# GET SAVING DETAIL
@api_view(['GET'])
@login_required
def get_detail_saving_account(request, pk):
    active_account = SavingAccount.objects.filter(account_id=pk).select_related('saving_type').select_related('member').get()

    serilizer = serilizers.SavingAccountSerilizer(active_account, many=False)
    return Response(serilizer.data)

# DEPOSIT MONEY FOR COMPOLSORY 
@login_required
@api_view(['PUT'])
def deposit_to_compulsory(request, pk, id):
    
    member = Member.objects.filter(member_id=id).get()
    compulsory = CompulsorySaving.objects.filter(account_id=pk).select_related('member').get()
    data = request.data
    balance = float( data['balance'])
    total_balance =  compulsory.balance + balance
    
    saving_count = member.save_count + 1

    if member.has_saved:
        return Response(status=400, data='Memeber has alrady saved') 

    if saving_count == 1:
        compulsory.balance = total_balance
        member.has_saved = True
        compulsory.save()
        member.save()

    else:
        amount = saving_count * 500
        if balance == amount:
            member.save_count = 0
            member.has_saved = True

            member.save()

            compulsory.balance = total_balance
            compulsory.save()

        else:
            reminder = balance / 500
            save_count = (member.save_count + 1) - reminder
            member.save_count = save_count

            print('save count', save_count)
            
            member.has_saved = True

            member.save()

            compulsory.balance = total_balance
            compulsory.save()
    
    tarnsaction = CompulsoryTransaction()
    tarnsaction.deposit = data['balance']
    tarnsaction.account = compulsory
    tarnsaction.balance = total_balance
    tarnsaction.save()

    compulsory_vault_deposit(balance)

    return Response(status=200, data='diposited')
    

# WITHDRAW MONEY FOR COMPOLSORY
@api_view(['PUT'])
@login_required
def withdraw_from_compulsory(request, pk):
    saving_account = CompulsorySaving.objects.filter(account_id=pk).select_related('member').get()
    data = request.data
    balance = float(data['balance'])
    total_balance = saving_account.balance - balance

    if saving_account.is_suspended:
        return Response(status=404, data='account is suspended')

    else:
        if balance <= saving_account.balance:
            if saving_account.is_suspended:
               return Response(status=404, data='account is susupended')

            else:
                saving_account.balance = total_balance

                saving_account.save()

                tarnsaction = CompulsoryTransaction()
                tarnsaction.withdraw = data['balance']
                tarnsaction.account = saving_account
                tarnsaction.balance = total_balance
                tarnsaction.save()
                compulsory_vault_withdraw(balance)
                return Response(status=200, data='withdraw')
       
        else:
         return Response(status=404, data='Small ammount')

# DEPOSIT MONEY FOR OTHER SAVING  
@api_view(['PUT'])
@login_required
def deposite_to_savings(request, pk):
    saving = SavingAccount.objects.filter(account_id=pk).select_related('member').get()
    
    if saving.is_active:
        data = request.data
        
        balance = float(data['balance'])
        total_balance = saving.balance + balance
        saving.balance = total_balance

        saving.save()

        tarnsaction = SavingTransaction()
        tarnsaction.deposit = data['balance']
        tarnsaction.account = saving
        tarnsaction.balance = total_balance
        tarnsaction.save()

        saving_vault_deposit(balance)

        return Response(status=200, data='diposited')
    else:
        return Response(status=404, data='Active is not active')

# WITHDRAW MONEY FOR OTHER SAVING  
@api_view(['PUT'])
@login_required
def withdraw_to_savings(request, pk):
    saving_account = SavingAccount.objects.filter(account_id=pk).select_related('member').get()
    data = request.data

    balance = float(data['balance'])
    total_balance = saving_account.balance - balance

    if saving_account.is_suspended:
        return Response(status=404, data='account is suspended')

    else:
        
        if balance <= saving_account.balance:
            saving_account.balance = total_balance

            saving_account.save()

            tarnsaction = SavingTransaction()
            tarnsaction.withdraw = data['balance']
            tarnsaction.account = saving_account
            tarnsaction.balance = total_balance
            tarnsaction.save()

            saving_vault_withdraw(balance)
            
            return Response(status=200, data='withdraw')
       
        else:
         return Response(status=404, data='Small ammount')

# MEMBERS MANDATORY SAVING MONTHLY CHECK
members_lists = []
@api_view(['POST'])
@login_required
def members_savings(request):
    
    start = request.POST.get('start')
    end = request.POST.get('end')

    monthly_saving = Member.objects.filter(compulsorysaving__compulsorytransaction__created_date__range =(start, end)).order_by('-compulsorysaving__compulsorytransaction__created_date')
    all_members = Member.objects.all()

    not_saved = []
    savings = list(monthly_saving)

    for member in all_members:
        check = savings.__contains__(member)
        if check is not True:
             not_saved.append(member)
    
    global members_lists
    members_lists = not_saved
    
    serilizer = serilizers.MemberSerilizer(not_saved, many=True)

    return Response(serilizer.data)

@api_view(["GET"])
@login_required
def change_save_counts(request):
    not_saved = members_lists
    change_saving_count(not_saved)
    
    return Response('accounts')

@api_view(['GET'])
@login_required
def check_has_saved(request):
    Member.objects.all().update(
        has_saved=False
    )

    return Response('zeroed')

@api_view(['GET'])
def get_member_id(request):

    id = get_savings_id()

    return Response({'id':id})

