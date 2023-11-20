from django.contrib import admin
from . import models

admin.site.register(models.Cashflow)

admin.site.register(models.CashflowType)

admin.site.register(models.TransactionPlanned)

admin.site.register(models.TransactionType)


admin.site.register(models.BankAccount)
