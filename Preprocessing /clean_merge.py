import pandas as pd

# Define file paths
data_dir = r"C:\Users\Anam\Desktop\New folder\ML PROJECT_GLACIER\GLACIER DATA"
output_file = f"{data_dir}\\glacier_mass_balance_final_cleaned.csv"

# Load datasets
mass_balance = pd.read_csv(f"{data_dir}\\mass_balance.csv")
mass_balance_overview = pd.read_csv(f"{data_dir}\\mass_balance_overview.csv")
mass_balance_point = pd.read_csv(f"{data_dir}\\mass_balance_point.csv")

# Standardize column names
mass_balance.rename(columns={'NAME': 'GLACIER_NAME', 'ANNUAL_BALANCE_UNC': 'UNCERTAINTY'}, inplace=True)
mass_balance_overview.rename(columns={'NAME': 'GLACIER_NAME'}, inplace=True)
mass_balance_point.rename(columns={'NAME': 'GLACIER_NAME'}, inplace=True)

# Select relevant columns
mass_balance = mass_balance[['WGMS_ID', 'GLACIER_NAME', 'YEAR', 'ANNUAL_BALANCE', 'UNCERTAINTY']]
mass_balance_overview = mass_balance_overview[['WGMS_ID', 'GLACIER_NAME', 'POLITICAL_UNIT', 'ELA', 'ELA_UNC']].drop_duplicates()

# Fill missing values in UNCERTAINTY
mass_balance['UNCERTAINTY'].fillna(mass_balance['UNCERTAINTY'].mean(), inplace=True)

# Merge datasets
merged_df = mass_balance.merge(mass_balance_overview, on=['WGMS_ID', 'GLACIER_NAME'], how='left')
merged_df = merged_df.merge(mass_balance_point, on=['WGMS_ID', 'GLACIER_NAME', 'YEAR'], how='left')

# Drop duplicate political unit column
merged_df.drop(columns=['POLITICAL_UNIT_y'], inplace=True)
merged_df.rename(columns={'POLITICAL_UNIT_x': 'POLITICAL_UNIT'}, inplace=True)

# Fill missing values
merged_df['ELA_UNC'] = merged_df['ELA_UNC'].fillna(merged_df['ELA_UNC'].median())  # ✅ Fix: No inplace=True

# Fill missing ELA values using the mean per glacier
merged_df['ELA'] = merged_df.groupby('GLACIER_NAME')['ELA'].transform(lambda x: x.fillna(x.mean()))

# Drop non-essential columns if they exist
merged_df.drop(columns=[col for col in ['BALANCE_CODE', 'REMARKS'] if col in merged_df.columns], inplace=True)

# Print final dataset preview
print("Final cleaned dataset preview:")
print(merged_df.head())

# Print remaining missing values
print("Missing values after cleaning:\n", merged_df.isna().sum())

# Save cleaned dataset
merged_df.to_csv(output_file, index=False)
