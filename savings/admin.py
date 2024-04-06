from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.SavingAccount)
admin.site.register(models.SavingTransaction)
admin.site.register(models.SavingType)

admin.site.register(models.CompulsorySaving)
admin.site.register(models.CompulsoryTransaction)

admin.site.register(models.SavingVault)
admin.site.register(models.SavingVaultTransaction)

