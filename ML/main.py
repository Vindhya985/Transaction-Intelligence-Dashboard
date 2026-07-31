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


def preprocessing(file_path):
    df = pd.read_csv(file_path)

    df = fill_missing_financials(df)
    df = fill_missing_descriptions(df)
    df = ensure_unique_ids(df)
    df = format_dates_and_columns(df)
    df = clean_descriptions(df)

    validate(df)

    return df