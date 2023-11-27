from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .constants import payment_term_multipliers


class TransactionCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    CASHFLOW_TYPE_CHOICES = [
        ('income_planned', 'Inkomen vast'),
        ('income_variable', 'Inkomen variabel'),
        ('spending_planned', 'Uitgaven vast'),
        ('spending_variable_planned', 'Uitgaven variabel gepland'),
        ('spending_variable_unplanned', 'Uitgaven variabel ongepland')
    ]
    id = models.CharField
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
    def validate_payment_term(value):
        valid_choices = ', '.join(
            payment_term_multipliers.keys())
        if value not in payment_term_multipliers:
            raise ValidationError(
                f"'{value}' is not a valid payment term. Valid choices are: {valid_choices}")
    payment_term_choices = [
        (key, key.replace('-', ' ').capitalize()) for key in payment_term_multipliers.keys()
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    payment_term = models.CharField(
        max_length=255,
        choices=payment_term_choices,
        validators=[validate_payment_term]
    )
    date_valid_from = models.DateField()
    date_valid_up_including = models.DateField(null=True)
    category = models.ForeignKey(TransactionCategory, on_delete=models.PROTECT)
    description = models.TextField(null=True)
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.PROTECT)
    last_update = models.DateTimeField(auto_now=True)


class TransactionVariable(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(TransactionCategory, on_delete=models.PROTECT)
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
    last_update = models.DateTimeField(auto_now=True)
