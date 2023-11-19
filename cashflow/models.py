from django.db import models

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
    cashflow_amount = models.DecimalField(max_digits=100, decimal_places=2)
    cashflow_payment_term = models.CharField(max_length=255, null=True)
    cashflow_valid_from = models.DateField()
    cashflow_valid_up_including = models.DateField(null=True)
    cashflow_description = models.TextField(null=True)
    cashflow_category_id = models.CharField(max_length=30)
    cashflow_type = models.ForeignKey(CashflowType, on_delete=models.PROTECT)
    cashflow_last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.id

    class Meta:
        ordering = ['id']
