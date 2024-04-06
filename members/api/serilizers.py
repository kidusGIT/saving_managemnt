from rest_framework.serializers import ModelSerializer
from members.models import Member

class MemberSerilizer(ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
