from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required 

from members.models import Member
from savings.models import SavingAccount, CompulsorySaving
from employees.models import *

@login_required
def credit_list(request):
    employee_id = request.user.employee_id
    employee = Employee.objects.get(employee_id=employee_id)

    if not employee.is_credit_class:
        
        return redirect('home-page')

    return render(request, 'credit_class_list.html')

@login_required
def credit_info(request, pk):
    employee_id = request.user.employee_id
    employee = Employee.objects.get(employee_id=employee_id)

    if not employee.is_credit_class:
        return redirect('home-page')

    member = Member.objects.get(member_id=pk)

    context = {
        'first_name':member.first_name,
        'father_name':member.father_name,
        'garnd_father_name':member.garnd_father_name,
        # address 
        'city':member.city,
        'sub_city':member.sub_city,
        'woreda':member.woreda,
        'house_num':member.house_num,

        'email':member.email,
        'phone_num':member.phone_num,
        'age':member.age,
    }     
    
    full_name = member.first_name + ' ' + member.father_name

    complsory = CompulsorySaving.objects.get(member = pk)
    saving = SavingAccount.objects.get(member = pk, is_active = True)

    return render(request, 'credit_info.html', {'member':context, 'full_name':full_name, 
        'id':pk, 'compulsory':complsory.account_id, 'saving':saving.account_id, 'saving_status':saving.is_suspended, 'comp_status':complsory.is_suspended})

@login_required
@api_view(['POST'])
def susspend_member(request):
    employee_id = request.user.employee_id
    employee = Employee.objects.get(employee_id=employee_id)

    if not employee.is_credit_class:
        return redirect('home-page')

    data = request.data

    saving = int(data['saving'])
    save_id = int(data['save_id'])

    compulsory = int(data['compulsory'])
    comp_id = int(data['comp_id'])
    
    if saving == 1:
        save = SavingAccount.objects.get(account_id = save_id, is_active = True)
        save.is_suspended = True
        save.save()

    elif saving == 2:
        save = SavingAccount.objects.get(account_id = save_id, is_active = True)
        save.is_suspended = False
        save.save()
       
        
    # COMPULSORY
    if compulsory == 1:
        complsory = CompulsorySaving.objects.get(account_id = comp_id)
        complsory.is_suspended = True
        complsory.save()

    elif compulsory == 2:
        complsory = CompulsorySaving.objects.get(account_id = comp_id)
        complsory.is_suspended = False
        complsory.save()
      
    return Response('suspended')