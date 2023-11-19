# Generated by Django 4.2.4 on 2023-11-15 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashflowType',
            fields=[
                ('cashflow_type_id', models.CharField(choices=[('income_fixed', 'Inkomen vast'), ('income_variable', 'Inkomen variabel'), ('spendings_fixed', 'Uitgaven vast'), ('spendings_variable_planned', 'Uitgaven variabel gepland'), ('spendings_variable_unplanned', 'Uitgaven variabel ongepland')], max_length=30, primary_key=True, serialize=False)),
                ('cashflow_type', models.CharField(choices=[('income', 'Inkomen'), ('spending', 'Uitgave')], max_length=30)),
                ('cashflow_subtype', models.CharField(choices=[('fixed', 'Vast'), ('variable', 'Variabel')], max_length=30)),
                ('cashflow_is_planned', models.IntegerField()),
            ],
            options={
                'ordering': ['cashflow_type_id'],
            },
        ),
        migrations.CreateModel(
            name='Cashflow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cashflow_amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('cashflow_payment_term', models.CharField(max_length=255, null=True)),
                ('cashflow_valid_from', models.DateField()),
                ('cashflow_valid_up_including', models.DateField(null=True)),
                ('cashflow_description', models.TextField(null=True)),
                ('cashflow_category_id', models.CharField(max_length=30)),
                ('cashflow_last_update', models.DateTimeField(auto_now=True)),
                ('cashflow_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cashflow.cashflowtype')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
