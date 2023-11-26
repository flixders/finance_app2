from django.contrib import admin
from . import models

admin.site.register(models.TransactionPlanned)

admin.site.register(models.TransactionVariable)

admin.site.register(models.TransactionType)

admin.site.register(models.BankAccount)
