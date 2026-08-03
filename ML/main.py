import pandas as pd


# 1. Fill missing numerical values in Debit and Credit
def fill_missing_financials(df):
    df['Debit'] = df['Debit'].fillna(0.0)
    df['Credit'] = df['Credit'].fillna(0.0)
    return df


# 2. Fill missing text descriptions and categories
def fill_missing_descriptions(df):
    df['Category'] = df['Category'].fillna('Uncategorized')
    df['Description'] = df['Description'].fillna('Unknown')
    return df


# 3. Drop duplicate rows and maintain unique transaction IDs
def ensure_unique_ids(df):
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset=['Transaction_ID'])
    return df


# 4. Standardize date formats and float conversions
def format_dates_and_columns(df):
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    numeric_cols = ['Debit', 'Credit', 'Balance']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    return df


# 5. Trim whitespace and apply title casing to transaction descriptions
def clean_descriptions(df):
    df['Description'] = df['Description'].astype(str).str.strip().str.title()
    return df


# 6. Validate processed dataset
def validate(df):
    assert not df['Transaction_ID'].duplicated().any(), "Duplicate Transaction_IDs found!"
    assert df['Debit'].isnull().sum() == 0, "Missing values found in Debit column!"
    assert df['Credit'].isnull().sum() == 0, "Missing values found in Credit column!"


def preprocessing(df):

    df = fill_missing_financials(df)
    df = fill_missing_descriptions(df)
    df = ensure_unique_ids(df)
    df = format_dates_and_columns(df)
    df = clean_descriptions(df)

    validate(df)

    return df

def get_transaction_summary(df):
    df['Data'] = pd.to_datetime(df['Date'])

    # total spending (debit) and total income (credit)
    total_spending = df['Debit'].sum()
    total_income = df['Credit'].sum()

    # no.of transactions
    num_transactions = len(df)

    # highest,lowest and average transaction amounts
    highest_transaction = df['Debit'].max()
    lowest_transaction = df['Debit'].min()
    average_transaction = df['Debit'].mean()

    # daily spending(total debit grouped by date)
    daily_spending = df.groupby(df['Data'].dt.date)['Debit'].sum().to_dict()

    # monthly spending(total debit grouped by year month)
    monthly_spending = df.groupby(df['Data'].dt.to_period('M'))['Debit'].sum().to_dict()

    # convert period  keys to string format
    monthly_spending = {str(k): v for k, v in monthly_spending.items()}


    return {
        "total_spending":   round(total_spending, 2),
        "total_income": round(total_income, 2),
        "num_transactions": num_transactions,
        "highest_transaction": round(highest_transaction, 2),
        "lowest_transaction": round(lowest_transaction, 2),
        "average_transaction": round(average_transaction, 2),
        "daily spending": daily_spending,
        "monthly spending": monthly_spending,
    }
