

# IMPORT MODLUES HERE
from savings.models import CompulsorySaving, SavingAccount, SavingTransaction, SavingVault, SavingVaultTransaction
from members.models import Member

def get_compulsory_id():
    last_entry = CompulsorySaving.objects.all().order_by('account_id').last()

    if last_entry:
        return last_entry.account_id + 1

    return 10000000

def get_savings_id():
    last_entry = SavingAccount.objects.all().order_by('account_id').last()

    if last_entry:
        return last_entry.account_id + 1

    return 10000000

def create_account(data):
    print(data['account_id'])
    

def change_account():
    pass

def change_transaction(active):
    active_account = SavingAccount.objects.filter(account_id=active).select_related('saving_type').select_related('member').get()
    
    if active_account.is_suspended:
        return -1
    else:
        active_account.is_active = False
        balance = active_account.balance
        active_account.balance = 0.0
        active_account.save()

        transaction = SavingTransaction()
        transaction.withdraw = balance
        transaction.account = active_account
        transaction.balance = balance
        transaction.save()

        return balance

def change_saving_count(not_savig):
    for saved in not_savig:
        member = Member.objects.get(member_id=saved.member_id)
        member.save_count = member.save_count + 1
        member.has_saved = False
        member.save()

# DEPOSIT
def saving_vault_deposit(balance):
    saving = SavingVault.objects.get(id=2)
    total_balance = saving.balance + balance
    saving.balance = total_balance
    saving.save()

    transaction = SavingVaultTransaction()
    transaction.account = saving
    transaction.deposit = balance
    transaction.balance = total_balance
    transaction.save() 

def compulsory_vault_deposit(balance):
    saving = SavingVault.objects.get(id=1)
    total_balance = saving.balance + balance
    saving.balance = total_balance
    saving.save()

    transaction = SavingVaultTransaction()
    transaction.account = saving
    transaction.deposit = balance
    transaction.balance = total_balance
    transaction.save() 

# WITHDRAW
def saving_vault_withdraw(balance):
    saving = SavingVault.objects.get(id=2)
    total_balance = saving.balance - balance
    saving.balance = total_balance
    saving.save()

    transaction = SavingVaultTransaction()
    transaction.account = saving
    transaction.withdraw = balance
    transaction.balance = total_balance
    transaction.save() 

def compulsory_vault_withdraw(balance):
    saving = SavingVault.objects.get(id=1)
    total_balance = saving.balance - balance
    saving.balance = total_balance
    saving.save()

    transaction = SavingVaultTransaction()
    transaction.account = saving
    transaction.withdraw = balance
    transaction.balance = total_balance
    transaction.save() 



    

