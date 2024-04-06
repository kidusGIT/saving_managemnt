from django.db import models

# Create your models here.

class Member(models.Model):
    member_id = models.IntegerField(primary_key=True, unique=True)

    # Name
    first_name = models.CharField(max_length=225)
    father_name = models.CharField(max_length=225)
    garnd_father_name = models.CharField(max_length=225)

    # Address
    city = models.CharField(max_length=225)
    sub_city = models.CharField(max_length=225)
    woreda = models.CharField(max_length=225)
    house_num = models.IntegerField(default=0)

    save_count = models.IntegerField(default=0)
    # HAS SAVED FOR THE CURRENT MONTH
    has_saved = models.BooleanField(default=False)
    email = models.EmailField(default='')
    phone_num =   models.IntegerField()
    age = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.father_name + " " + self.garnd_father_name
