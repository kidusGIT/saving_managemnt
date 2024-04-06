from django.db import models

# Create your models here.
class TimeStamp(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def __str__(self):
        return str(self.start) + ' ' + str(self.end)
