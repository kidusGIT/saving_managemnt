from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# IMPORT MODULES HERE
from savings.models import SavingVaultTransaction
from employees.models import Employee

# views 
@login_required
def manager_home(request):
    employee_id = request.user.employee_id
    employee = Employee.objects.get(employee_id=employee_id)

    if not employee.is_manager:
        return redirect('home-page')
    
    saving_transaction = SavingVaultTransaction.objects.filter(account = 2).select_related('account')
    compulsory_transaction = SavingVaultTransaction.objects.filter(account = 1).select_related('account')

    total_balance = saving_transaction[0].account.balance + compulsory_transaction[0].account.balance

    return render(request, 'manager_index.html', {'saving_transaction':saving_transaction, 'compulsory_transaction':compulsory_transaction,
        'saving_balance':saving_transaction[0].account.balance, 'comulsory':compulsory_transaction[0].account.balance,
        'total_balance':total_balance})

