from django.db import models
from django.utils import timezone

# IMPORT MODULES HERE
from members.models import Member

# SAVING TYPE
class SavingType(models.Model):
    account_name = models.CharField(max_length=225, unique=True)

    def __str__(self):
        return self.account_name 

# SAVINGS
class SavingAccount(models.Model):
    account_id = models.IntegerField(primary_key=True, unique=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    saving_type = models.ForeignKey(SavingType, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    is_suspended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member.first_name + ' ' + self.saving_type.account_name 

# SAVING TRANSACTIONS
class SavingTransaction(models.Model):
    account = models.ForeignKey(SavingAccount, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    withdraw = models.FloatField(default=0.0)
    deposit = models.FloatField(default=0.0)
    interest = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.member.first_name + ' ' + self.account.saving_type.account_name
    
# ------------------------- /// ---------------------------- \\\ ------------------------------

# COMPULSORY SAVING
class CompulsorySaving(models.Model):
    account_id = models.IntegerField(primary_key=True, unique=True)
    member = models.OneToOneField(Member, on_delete=models.CASCADE, unique=True)
    balance = models.FloatField(default=0.0)
    is_suspended = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  str(self.account_id) + " " + self.member.first_name
    
# COMPULSORY TRANSACTIONS
class CompulsoryTransaction(models.Model):
    account = models.ForeignKey(CompulsorySaving, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    withdraw = models.FloatField(default=0.0)
    deposit = models.FloatField(default=0.0)
    interest = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.member.first_name 
    
# SAVING VAULTS 
class SavingVault(models.Model):
    name = models.CharField(max_length=255)
    balance = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SavingVaultTransaction(models.Model):
    account = models.ForeignKey(SavingVault, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    withdraw = models.FloatField(default=0.0)
    deposit = models.FloatField(default=0.0)
    interest = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.name + ' ' + str(self.account.balance) 
 

