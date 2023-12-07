import pandas as pd
from .constants import payment_term_multipliers
from django.db.models import F


def calculate_budget(start_date, end_date, TransactionVariable, TransactionPlanned, user):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    queryset_variable = TransactionVariable.objects.filter(
        user=user,
        date__range=(start_date.date(), end_date.date())
    )

    queryset_fixed = TransactionPlanned.objects.filter(
        user=user,
        date_valid_up_including__gte=start_date.date()
    )

    data_variable = list(queryset_variable.values(
        'amount',
        'date'))
    df_variable = pd.DataFrame(data_variable)

    def assign_transaction_type(amount):
        if amount > 0:
            return 'variable_income'
        else:
            return 'variable_spending'
    df_variable['transaction_type_name'] = df_variable['amount'].apply(
        lambda x: assign_transaction_type(x))

    data_fixed = list(queryset_fixed.values(
        'amount',
        'date_valid_from',
        'date_valid_up_including',
        payment_term_name=F('payment_term__payment_term_name')))
    df_fixed = pd.DataFrame(data_fixed)

    df_fixed['yearly_amount'] = df_fixed.apply(
        lambda row: row['amount'] *
        payment_term_multipliers.get(row['payment_term_name'], pd.NA),
        axis=1
    )
    df_fixed['amount'] = df_fixed['yearly_amount'] / 365
    df_fixed['date_valid_from'] = pd.to_datetime(
        df_fixed['date_valid_from'])

    df_fixed['date_valid_up_including'] = end_date
    df_fixed['date_valid_up_including'] = pd.to_datetime(
        df_fixed['date_valid_up_including'])

    df_fixed['transaction_type_name'] = df_fixed['amount'].apply(
        lambda x: 'fixed_income' if x > 0 else 'fixed_spending'
    )

    df_fixed['date'] = df_fixed.apply(
        lambda row: pd.date_range(
            start=row['date_valid_from'],
            end=row['date_valid_up_including'],
            freq='D'),
        axis=1
    )
    df_fixed = df_fixed[[
        'amount',
        'date',
        'transaction_type_name']]
    df_fixed = df_fixed.explode('date')
    result_df = \
        pd.concat(
            [df_variable,
             df_fixed],
            ignore_index=True)

    result_df['date'] = pd.to_datetime(result_df['date'])
    result_df = \
        result_df[
            (result_df['date'] >= start_date)
            & (result_df['date'] <= end_date)]

    result_df = \
        result_df.groupby(['transaction_type_name'])[
            'amount'].sum().reset_index()

    result_total = result_df['amount'].sum()
    available_budget_row = pd.DataFrame([{
        'transaction_type_name': 'available_budget',
        'amount': result_total
    }])
    transaction_type_mapping = {
        'fixed_income': 'Inkomen vast',
        'fixed_spending': 'Uitgaven vast',
        'variable_spending': 'Uitgaven variabel',
        'variable_income': 'Inkomen variabel',
        'available_budget': 'Beschikbaar budget',
    }

    result_df = pd.concat(
        [result_df, available_budget_row], ignore_index=True)

    result_df['transaction_type_title'] = result_df['transaction_type_name'].map(
        transaction_type_mapping)
    result_df
    return (result_df)
