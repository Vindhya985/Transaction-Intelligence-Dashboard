# read file using Pandas
import pandas as pd
df=pd.read_csv('sample-100-rows.csv')
# inspecting info
print(df.info())
print(df.head())

# handling missing values
print(df.isnull().sum())
# for example fill missing debit or credit values with 0
df['Debit'] = df['Debit'].fillna(0.0)
df['Credit'] = df['Credit'].fillna(0.0)
# fill the missing descriptions with defaults
df['Category'] = df['Category'].fillna('Uncategorized')
df['Description'] = df['Description'].fillna('Unknown')
# removing duplicates
# by dropping identical rows
df = df.drop_duplicates()
# ensure transaction IDs are unique
df = df.drop_duplicates(subset=['Transaction_ID'])
# format the date and amount columns
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
numeric_columns = ['Debit', 'Credit','Balance']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
# for clean transaction descriptions
df['Description'] = df['Description'].astype(str).str.strip().str.title()
assert not df['Transaction_ID'].duplicated().any(), "Duplicate Transaction_IDs found!"
assert df['Debit'].isnull().sum() == 0, "Missing values found in Debit column!"
assert df['Credit'].isnull().sum() == 0, "Missing values found in Credit column!"
df.to_csv('cleaned_sample_100_rows.csv', index=False)
pd.set_option('display.max_columns', None)
pd.set_option('display.width',1000)
print("All checks passed. Cleaned data saved to 'cleaned_sample_100_rows.csv'.")
print("DATA PROCESSING COMPLETED")
print(df.info())
print(df.head())
