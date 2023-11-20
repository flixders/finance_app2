from django.db import models
from django.contrib.auth.models import User

CASHFLOW_TYPE_CHOICES = [
    ('income_fixed', 'Inkomen vast'),
    ('income_variable', 'Inkomen variabel'),
    ('spendings_fixed', 'Uitgaven vast'),
    ('spendings_variable_planned', 'Uitgaven variabel gepland'),
    ('spendings_variable_unplanned', 'Uitgaven variabel ongepland')
]


class CashflowType(models.Model):
    CASHFLOW_TYPES = [
        ('income', 'Inkomen'),
        ('spending', 'Uitgave')
    ]
    CASHFLOW_SUBTYPES = [
        ('fixed', 'Vast'),
        ('variable', 'Variabel')
    ]
    cashflow_type_id = models.CharField(
        max_length=30, primary_key=True, choices=CASHFLOW_TYPE_CHOICES)
    cashflow_type = models.CharField(max_length=30, choices=CASHFLOW_TYPES)
    cashflow_subtype = models.CharField(
        max_length=30, choices=CASHFLOW_SUBTYPES)
    cashflow_is_planned = models.IntegerField()

    def __str__(self) -> str:
        return self.cashflow_type_id

    class Meta:
        ordering = ['cashflow_type_id']


class Cashflow(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cashflow_amount = models.DecimalField(max_digits=100, decimal_places=2)
    cashflow_payment_term = models.CharField(max_length=255, null=True)
    cashflow_valid_from = models.DateField()
    cashflow_valid_up_including = models.DateField(null=True)
    cashflow_description = models.TextField(null=True)
    cashflow_category_id = models.CharField(max_length=30, null=True)
    cashflow_type = models.ForeignKey(CashflowType, on_delete=models.PROTECT)
    cashflow_last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.id

    class Meta:
        ordering = ['id']


class TransactionType(models.Model):
    CASHFLOW_TYPE_CHOICES = [
        ('income_fixed', 'Inkomen vast'),
        ('income_variable', 'Inkomen variabel'),
        ('spendings_fixed', 'Uitgaven vast'),
        ('spendings_variable_planned', 'Uitgaven variabel gepland'),
        ('spendings_variable_unplanned', 'Uitgaven variabel ongepland')
    ]
    transaction_type_id = models.CharField(
        max_length=30, primary_key=True, choices=CASHFLOW_TYPE_CHOICES)
    type_name = models.CharField(max_length=30)
    subtype_name = models.CharField(
        max_length=30)
    is_planned = models.IntegerField()

    def __str__(self) -> str:
        return self.transaction_type_id

    class Meta:
        ordering = ['transaction_type_id']


class TransactionPlanned(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    payment_term = models.CharField(max_length=255, null=True)
    date_valid_from = models.DateField()
    date_valid_up_including = models.DateField(null=True)
    description = models.TextField(null=True)
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.PROTECT)
    last_update = models.DateTimeField(auto_now=True)


class TransactionVariable(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField()
    description = models.TextField(null=True)
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.PROTECT)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.id

    class Meta:
        ordering = ['id']


class BankAccount(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField()
