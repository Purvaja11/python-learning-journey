"""
Day 11 Advanced Challenge: Clean Real Sales Data
This simulates actual messy sales data you'd encounter in a job!
"""

import pandas as pd
import numpy as np

# Generate realistic messy sales data
np.random.seed(100)

sales_data = pd.DataFrame({
    'Order_ID': ['ORD001', 'ORD002', 'ORD003', 'ORD002', 'ORD004', None, 'ORD005', 'ORD006', 'ORD007', 'ORD008'],
    'Customer_Name': ['  Raj Kumar  ', 'priya SHARMA', 'amit@verma', 'Priya Sharma', 
                      'sneha GUPTA', 'Vikram Singh', 'raj kumar', '  Neha Patel', 
                      'Rohit$Sharma', 'Anjali Das'],
    'Product': ['Laptop', 'phone', 'TABLET', 'Phone', 'laptop', 'Headphones', 
                'Mouse', 'Keyboard', 'Monitor', 'laptop'],
    'Quantity': [2, 1, 3, 1, -1, 5, 10, np.nan, 2, 1000],  # Issues: negative, missing, outlier
    'Price': [50000, 25000, 15000, 25000, 50000, np.nan, 500, 1200, 12000, 50000],
    'Discount_Percent': [10, 5, 15, 5, 999, 20, 0, 10, 5, 10],  # Outlier: 999%
    'Order_Date': ['2024-01-15', '2024-01-20', 'invalid', '2024-01-20', 
                   '2024-02-01', '2024-02-05', '2024-01-15', '2024-03-10',
                   '2024-03-15', '2050-12-31'],  # Future date issue
    'City': ['  mumbai  ', 'DELHI', 'bangalore', 'Delhi', 'mumbai', 
             'Pune', 'Chennai', 'bangalore', 'Mumbai', 'Delhi'],
    'Payment_Status': ['Paid', 'paid', 'PENDING', 'Paid', 'pending', 
                       'Failed', 'Paid', None, 'Paid', 'paid']
})

print("="*80)
print("MESSY SALES DATA - YOUR CHALLENGE!")
print("="*80)
print(sales_data)

# Calculate what should be the total revenue (before cleaning)
print("\n" + "="*80)
print("DATA QUALITY ISSUES TO IDENTIFY AND FIX:")
print("="*80)

issues_list = """
YOUR TASK: Identify and document ALL issues, then clean the data!

Issues to find:
1. ❌ Missing values
2. ❌ Duplicate orders
3. ❌ Negative quantities
4. ❌ Outlier quantities (1000 laptops?)
5. ❌ Invalid discount (999%)
6. ❌ Invalid/future dates
7. ❌ Inconsistent product names (phone vs Phone vs PHONE)
8. ❌ Inconsistent customer names (extra spaces, special chars)
9. ❌ Inconsistent city names
10. ❌ Inconsistent payment status

CLEANING STEPS:
"""

print(issues_list)

# Solution code starts here
print("\n" + "="*80)
print("STEP-BY-STEP CLEANING SOLUTION")
print("="*80)

df = sales_data.copy()

print("\n1️⃣ INITIAL DATA PROFILE")
print("-" * 80)
print(f"Shape: {df.shape}")
print(f"Missing values:\n{df.isnull().sum()}")
print(f"Duplicates: {df.duplicated().sum()}")

# Step 1: Remove exact duplicates
print("\n2️⃣ REMOVING DUPLICATES")
print("-" * 80)
duplicates_before = df.duplicated().sum()
df = df.drop_duplicates()
print(f"✓ Removed {duplicates_before} duplicate rows")
print(f"New shape: {df.shape}")

# Step 2: Handle missing Order_ID
print("\n3️⃣ HANDLING MISSING ORDER_ID")
print("-" * 80)
missing_id = df['Order_ID'].isnull().sum()
if missing_id > 0:
    print(f"Found {missing_id} missing Order_IDs")
    # Generate new IDs for missing ones
    max_id = int(df['Order_ID'].dropna().str.replace('ORD', '').max())
    for idx in df[df['Order_ID'].isnull()].index:
        max_id += 1
        df.loc[idx, 'Order_ID'] = f'ORD{max_id:03d}'
    print(f"✓ Generated new Order_IDs for missing values")

# Step 3: Clean Customer Names
print("\n4️⃣ CLEANING CUSTOMER NAMES")
print("-" * 80)
print(f"Before: {df['Customer_Name'].head(3).tolist()}")
df['Customer_Name'] = df['Customer_Name'].str.strip()
df['Customer_Name'] = df['Customer_Name'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
df['Customer_Name'] = df['Customer_Name'].str.title()
print(f"After: {df['Customer_Name'].head(3).tolist()}")
print("✓ Removed special characters, whitespace, standardized case")

# Step 4: Standardize Product Names
print("\n5️⃣ STANDARDIZING PRODUCT NAMES")
print("-" * 80)
print(f"Unique products before: {df['Product'].unique()}")
df['Product'] = df['Product'].str.strip().str.title()
print(f"Unique products after: {df['Product'].unique()}")
print("✓ Standardized product names")

# Step 5: Fix Quantity Issues
print("\n6️⃣ FIXING QUANTITY ISSUES")
print("-" * 80)

# Handle missing quantities
missing_qty = df['Quantity'].isnull().sum()
if missing_qty > 0:
    df['Quantity'] = df['Quantity'].fillna(1)
    print(f"✓ Filled {missing_qty} missing quantities with 1")

# Remove negative quantities
negative_qty = (df['Quantity'] < 0).sum()
if negative_qty > 0:
    df = df[df['Quantity'] >= 0]
    print(f"✓ Removed {negative_qty} rows with negative quantities")

# Handle outliers (quantity > 100 is suspicious)
Q1 = df['Quantity'].quantile(0.25)
Q3 = df['Quantity'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR

outliers = df[df['Quantity'] > upper_bound]
print(f"✓ Found {len(outliers)} quantity outliers (> {upper_bound:.0f})")
print(f"  Outlier rows: {outliers[['Order_ID', 'Product', 'Quantity']].to_dict('records')}")

# Cap outliers
df['Quantity'] = df['Quantity'].clip(upper=100)
print(f"✓ Capped quantities at 100")

# Step 6: Fix Price Issues
print("\n7️⃣ FIXING PRICE ISSUES")
print("-" * 80)
missing_price = df['Price'].isnull().sum()
if missing_price > 0:
    # Fill with median price
    median_price = df['Price'].median()
    df['Price'] = df['Price'].fillna(median_price)
    print(f"✓ Filled {missing_price} missing prices with median: ₹{median_price:,.0f}")

# Step 7: Fix Discount Issues
print("\n8️⃣ FIXING DISCOUNT ISSUES")
print("-" * 80)
invalid_discount = (df['Discount_Percent'] > 100).sum()
if invalid_discount > 0:
    print(f"Found {invalid_discount} invalid discounts (> 100%)")
    df['Discount_Percent'] = df['Discount_Percent'].clip(upper=50)
    print("✓ Capped discounts at 50%")

# Step 8: Fix Date Issues
print("\n9️⃣ FIXING DATE ISSUES")
print("-" * 80)
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
print(f"✓ Converted to datetime format")

# Remove future dates
today = pd.Timestamp.now()
future_dates = (df['Order_Date'] > today).sum()
if future_dates > 0:
    print(f"Found {future_dates} future dates")
    df = df[df['Order_Date'] <= today]
    print("✓ Removed orders with future dates")

# Fill NaT with median date
if df['Order_Date'].isnull().sum() > 0:
    median_date = df['Order_Date'].median()
    df['Order_Date'] = df['Order_Date'].fillna(median_date)
    print(f"✓ Filled missing dates with median date")

# Step 9: Standardize City
print("\n🔟 STANDARDIZING CITIES")
print("-" * 80)
df['City'] = df['City'].str.strip().str.title()
print(f"✓ Standardized city names")
print(f"Unique cities: {df['City'].unique()}")

# Step 10: Standardize Payment Status
print("\n1️⃣1️⃣ STANDARDIZING PAYMENT STATUS")
print("-" * 80)
df['Payment_Status'] = df['Payment_Status'].str.strip().str.title()
missing_status = df['Payment_Status'].isnull().sum()
if missing_status > 0:
    df['Payment_Status'] = df['Payment_Status'].fillna('Pending')
    print(f"✓ Filled {missing_status} missing statuses with 'Pending'")
print(f"Payment status values: {df['Payment_Status'].unique()}")

# Step 11: Calculate Revenue
print("\n1️⃣2️⃣ CALCULATING REVENUE")
print("-" * 80)
df['Total_Amount'] = df['Quantity'] * df['Price']
df['Discount_Amount'] = df['Total_Amount'] * (df['Discount_Percent'] / 100)
df['Final_Amount'] = df['Total_Amount'] - df['Discount_Amount']
print("✓ Added calculated columns: Total_Amount, Discount_Amount, Final_Amount")

# Final validation
print("\n" + "="*80)
print("FINAL CLEANED DATASET")
print("="*80)
print(df)

print("\n" + "="*80)
print("CLEANING SUMMARY")
print("="*80)
print(f"Original rows: {len(sales_data)}")
print(f"Cleaned rows: {len(df)}")
print(f"Rows removed: {len(sales_data) - len(df)}")
print(f"\nMissing values: {df.isnull().sum().sum()}")
print(f"Duplicates: {df.duplicated().sum()}")

print("\n" + "="*80)
print("BUSINESS INSIGHTS")
print("="*80)
print(f"Total Revenue: ₹{df['Final_Amount'].sum():,.2f}")
print(f"Average Order Value: ₹{df['Final_Amount'].mean():,.2f}")
print(f"Total Orders: {len(df)}")
print(f"\nTop 3 Products by Revenue:")
print(df.groupby('Product')['Final_Amount'].sum().sort_values(ascending=False).head(3))
print(f"\nTop 3 Cities by Orders:")
print(df['City'].value_counts().head(3))

print("\n✅ DATA CLEANING COMPLETE!")
print("\n💡 YOUR TURN: Try modifying the cleaning logic!")
print("   - Change the outlier threshold")
print("   - Try different missing value strategies")
print("   - Add more validation rules")