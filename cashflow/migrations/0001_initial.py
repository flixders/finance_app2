# Generated by Django 4.2.7 on 2023-11-28 19:20

import cashflow.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('income_planned', 'Inkomen vast'), ('income_variable', 'Inkomen variabel'), ('spending_planned', 'Uitgaven vast'), ('spending_variable_planned', 'Uitgaven variabel gepland'), ('spending_variable_unplanned', 'Uitgaven variabel ongepland')], max_length=30)),
                ('main_name', models.CharField(max_length=30)),
                ('sub_name', models.CharField(max_length=30)),
                ('is_scheduled', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TransactionVariable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('date', models.DateField()),
                ('description', models.TextField(null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cashflow.transactioncategory')),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cashflow.transactiontype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TransactionPlanned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('payment_term', models.CharField(choices=[('monthly', 'Monthly'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('quarterly', 'Quarterly'), ('bi-weekly', 'Bi weekly'), ('semi-monthly', 'Semi monthly'), ('annually', 'Annually')], max_length=255, validators=[cashflow.models.TransactionPlanned.validate_payment_term])),
                ('date_valid_from', models.DateField()),
                ('date_valid_up_including', models.DateField(null=True)),
                ('description', models.TextField(null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cashflow.transactioncategory')),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cashflow.transactiontype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_balance', models.DecimalField(decimal_places=2, max_digits=100)),
                ('date', models.DateField()),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
