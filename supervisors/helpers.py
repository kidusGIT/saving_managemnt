# IMPORT MODLUES HERE
from members.models import Member

def change_saving_count(not_savig):
    for saved in not_savig:
        member = Member.objects.get(member_id=saved.member_id)
        member.save_count = member.save_count + 1
        member.has_saved = False
        member.save()