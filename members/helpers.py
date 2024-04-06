
# IMPORT USER MODUE HERE
from .models import Member


def get_id():
    last_entry = Member.objects.all().order_by('member_id').last()

    if last_entry:
        return last_entry.member_id + 1

    return 10000000

def create_members(first_name, father_name, garnd_father_name, city, 
    sub_city, woreda, house_num, phone_num, age, email, member_id):

    member = Member()
    member.member_id = member_id

    member.first_name = first_name
    member.father_name = father_name
    member.garnd_father_name = garnd_father_name

    member.city = city
    member.sub_city = sub_city
    member.woreda = woreda

    if(house_num != ''):
        member.house_num = house_num
    
    if(phone_num != ''):
        member.phone_num = phone_num
    member.age = age
    member.email = email

    member.save()

def update_members(first_name, father_name, garnd_father_name, city, 
        sub_city, woreda, house_num, phone_num, age, email, id):

    member = Member.objects.get(member_id=id)
    
    member.first_name = first_name
    member.father_name = father_name
    member.garnd_father_name = garnd_father_name

    member.city = city
    member.sub_city = sub_city
    member.woreda = woreda

    if(house_num != ''):
        member.house_num = house_num
    
    if(phone_num != ''):
        member.phone_num = phone_num
    member.age = age
    member.email = email

    member.save()
