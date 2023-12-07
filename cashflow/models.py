from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .constants import payment_term_multipliers
from datetime import date


class TransactionCategory(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class TransactionPaymentTerm(models.Model):
    payment_term_name = models.CharField(
        max_length=30)
    payment_term_name_dutch = models.CharField(
        max_length=30)


class TransactionPlanned(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    payment_term = models.ForeignKey(
        TransactionPaymentTerm, on_delete=models.PROTECT)
    category = models.ForeignKey(TransactionCategory, on_delete=models.PROTECT)
    date_valid_from = models.DateField()
    date_valid_up_including = models.DateField(null=True)
    description = models.TextField(null=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']


class TransactionVariable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(TransactionCategory, on_delete=models.PROTECT)
    description = models.TextField(null=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField()
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
