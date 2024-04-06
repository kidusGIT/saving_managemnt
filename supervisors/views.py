from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from saving_system_three.settings import EMAIL_HOST_USER
from datetime import datetime

# IMPORT USER BUILT MODULE HERE
from members.models import Member
from .models import TimeStamp
from savings import serilizers
from .serilizer import TimeStampSerializer
from .helpers import change_saving_count
from employees.models import Employee
from savings.models import CompulsoryTransaction


# HOME PAGE
@login_required
def index_page(request):
    employee_id = request.user.employee_id
    employee = Employee.objects.get(employee_id=employee_id)

    if not employee.is_saving_super:
        return redirect('home-page')

    return render(request, 'supervisor_home.html')

# MEMBERS COMPULSORY MONTHLY SAVING DISPLAY


@login_required
def compulsory_monthly_saving(request):

    employee_id = request.user.employee_id
    employee = Employee.objects.get(employee_id=employee_id)

    if not employee.is_saving_super:
        return redirect('home-page')

    timestamp = TimeStamp.objects.all()
    now = timezone.now()

    if timestamp[0].start > now:
        return render(request, 'time_out_page.html', {'start': timestamp[0].start, 'check': 1})

    if timestamp[0].start <= now and timestamp[0].end > now:
        return render(request, 'monthlySaving.html', {'end': timestamp[0].end})

    if timestamp[0].end < now:
        return render(request, 'time_out_page.html', {'start': timestamp[0].start, 'check': 0})


# MEMBERS MANDATORY SAVING MONTHLY CHECK
members_lists = []


@login_required
@api_view(['POST'])
def members_savings(request):

    start = request.POST.get('start_first')
    end = request.POST.get('end_first')

    start_time = datetime.fromisoformat(start)
    end_time = datetime.fromisoformat(end)

    monthly_saving = Member.objects.filter(compulsorysaving__compulsorytransaction__created_date__range=(
        start_time, end_time)).order_by('-compulsorysaving__compulsorytransaction__created_date')
    all_members = Member.objects.all()

    not_saved = []
    savings = list(monthly_saving)
    for member in all_members:
        check = savings.__contains__(member)
        if check is not True:
            # print(member.first_name)
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
def check_has_saved(request):
    Member.objects.all().update(
        has_saved=False
    )

    return Response('zeroed')

# MEMBERS LIST THAT DO NOT SAVE


@login_required
def members_list(request):

    employee_id = request.user.employee_id
    employee = Employee.objects.get(employee_id=employee_id)

    if not employee.is_saving_super:
        return redirect('home-page')

    return render(request, 'list_of_members.html')

# MEMEBRS THAT DO NOT SAVE


@api_view(['GET'])
@login_required
def members_that_do_not_save(request, amount):
    if amount >= 3:
        members = Member.objects.filter(save_count__gte=amount)
        serilizer = serilizers.MemberSerilizer(members, many=True)

        return Response(serilizer.data)

    members = Member.objects.filter(save_count__exact=amount)
    serilizer = serilizers.MemberSerilizer(members, many=True)

    return Response(serilizer.data)

# SET TIME FOR TIME STAMPS


@api_view(['POST'])
@login_required
def set_time(request):
    try:
        TimeStamp.objects.all().delete()
    except:
        pass

    seri = TimeStampSerializer(data=request.data)

    if seri.is_valid():
        seri.save()

    return Response(seri.data)


@api_view(['GET'])
@login_required
def get_time(request):
    time = TimeStamp.objects.all()

    seril = TimeStampSerializer(time, many=True)
    return Response(seril.data)

# SEND WARNING EMAIL TO MEMBERS


@login_required
@api_view(['GET'])
def send_email_to_member(request):

    members = Member.objects.filter(save_count__gte=3)

    emails = []
    for member in members:
        emails.append(member.email)

    send_mail(
        "Please Save",
        "Please do your saving properly",
        # message sender
        'gentekidu@gmail.com',
        # message reciver
        emails,
        fail_silently=False,
    )

    return Response('sented')
