import pandas as pd
import glob

# Step 1: Load all matching CSV files
files = glob.glob("data/daily_sales_data_*.csv")
df_list = [pd.read_csv(file) for file in files]
df = pd.concat(df_list, ignore_index=True)

# Step 2: Filter to only include 'pink morsel'
df = df[df['product'] == 'pink morsel']  # Make sure it's lowercase if needed

# Step 3: Convert 'price' from string (like '$10.00') to float
df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)

# Step 4: Calculate Sales = quantity * price
df['Sales'] = df['quantity'] * df['price']

# Step 5: Keep only needed columns
df_final = df[['Sales', 'date', 'region']]
df_final = df_final.rename(columns={'date': 'Date', 'region': 'Region'})

# Step 6: Sort by Date
df_final = df_final.sort_values(by='Date')

# Step 7: Export the result to CSV
output_path = "processed_sales.csv"
df_final.to_csv(output_path, index=False)

print(f"✅ Processed data saved to {output_path}")
