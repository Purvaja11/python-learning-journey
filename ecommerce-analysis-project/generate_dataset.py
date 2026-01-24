"""
E-commerce Customer Behavior Dataset Generator
Creates a realistic dataset similar to Kaggle datasets
This simulates downloading from Kaggle!
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

print("=" * 70)
print("🎯 GENERATING E-COMMERCE DATASET")
print("=" * 70)

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_CUSTOMERS = 1000
NUM_ORDERS = 5000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

print(f"\nGenerating dataset with:")
print(f"  - {NUM_CUSTOMERS} unique customers")
print(f"  - {NUM_ORDERS} orders")
print(f"  - Date range: {START_DATE.date()} to {END_DATE.date()}")

# ============================================================================
# GENERATE CUSTOMER DATA
# ============================================================================
print("\n📊 Step 1: Generating customer data...")

customer_ids = [f"CUST{str(i).zfill(5)}" for i in range(1, NUM_CUSTOMERS + 1)]

customers = pd.DataFrame({
    'Customer_ID': customer_ids,
    'Customer_Name': [f"Customer_{i}" for i in range(1, NUM_CUSTOMERS + 1)],
    'Age': np.random.randint(18, 70, NUM_CUSTOMERS),
    'Gender': np.random.choice(['Male', 'Female', 'Other'], NUM_CUSTOMERS, p=[0.48, 0.48, 0.04]),
    'City': np.random.choice([
        'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 
        'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Surat'
    ], NUM_CUSTOMERS),
    'Membership_Type': np.random.choice(
        ['Basic', 'Silver', 'Gold', 'Platinum'], 
        NUM_CUSTOMERS, 
        p=[0.5, 0.3, 0.15, 0.05]
    ),
    'Registration_Date': [
        START_DATE + timedelta(days=random.randint(0, 365))
        for _ in range(NUM_CUSTOMERS)
    ]
})

# Add some missing values (real-world messiness!)
customers.loc[random.sample(range(NUM_CUSTOMERS), 20), 'Age'] = np.nan
customers.loc[random.sample(range(NUM_CUSTOMERS), 15), 'City'] = None

print(f"✅ Generated {len(customers)} customer records")
print(f"   Columns: {list(customers.columns)}")


# ============================================================================
# GENERATE ORDER DATA
# ============================================================================
print("\n📦 Step 2: Generating order data...")

# Product catalog
products = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch'],
    'Clothing': ['Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes'],
    'Home': ['Sofa', 'Table', 'Chair', 'Lamp', 'Rug'],
    'Books': ['Fiction', 'Non-Fiction', 'Comics', 'Magazine', 'Textbook'],
    'Sports': ['Cricket Bat', 'Football', 'Yoga Mat', 'Dumbbells', 'Bicycle']
}

# Flatten products
all_products = [(cat, prod) for cat, prods in products.items() for prod in prods]

orders_data = []

for i in range(1, NUM_ORDERS + 1):
    customer_id = random.choice(customer_ids)
    category, product = random.choice(all_products)
    
    # Base prices by category
    base_prices = {
        'Electronics': (800, 50000),
        'Clothing': (500, 5000),
        'Home': (1000, 30000),
        'Books': (200, 1500),
        'Sports': (500, 15000)
    }
    
    min_price, max_price = base_prices[category]
    price = round(random.uniform(min_price, max_price), 2)
    quantity = random.randint(1, 5)
    total = round(price * quantity, 2)
    
    # Random date
    order_date = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
    
    # Delivery status
    status = random.choices(
        ['Delivered', 'Shipped', 'Processing', 'Cancelled', 'Returned'],
        weights=[0.7, 0.15, 0.05, 0.05, 0.05]
    )[0]
    
    # Payment method
    payment = random.choice(['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'COD'])
    
    # Discount (some orders)
    discount = random.choices([0, 5, 10, 15, 20], weights=[0.5, 0.2, 0.15, 0.1, 0.05])[0]
    
    # Rating (only for delivered orders)
    rating = random.randint(1, 5) if status == 'Delivered' else None
    
    orders_data.append({
        'Order_ID': f"ORD{str(i).zfill(6)}",
        'Customer_ID': customer_id,
        'Order_Date': order_date,
        'Category': category,
        'Product_Name': product,
        'Quantity': quantity,
        'Price': price,
        'Total_Amount': total,
        'Discount_Percent': discount,
        'Final_Amount': round(total * (1 - discount/100), 2),
        'Payment_Method': payment,
        'Order_Status': status,
        'Rating': rating
    })

orders = pd.DataFrame(orders_data)

# Add some missing values and data quality issues
orders.loc[random.sample(range(NUM_ORDERS), 50), 'Rating'] = np.nan
orders.loc[random.sample(range(NUM_ORDERS), 30), 'Discount_Percent'] = np.nan

# Add some data entry errors (typos in status)
error_indices = random.sample(range(NUM_ORDERS), 20)
orders.loc[error_indices, 'Order_Status'] = random.choice(['DELIVERED', 'delivered', 'Deliverd'])

print(f"✅ Generated {len(orders)} order records")
print(f"   Columns: {list(orders.columns)}")


# ============================================================================
# SAVE DATASETS
# ============================================================================
print("\n💾 Step 3: Saving datasets to CSV...")

customers.to_csv('ecommerce_customers.csv', index=False)
orders.to_csv('ecommerce_orders.csv', index=False)

print("✅ Saved files:")
print("   - ecommerce_customers.csv")
print("   - ecommerce_orders.csv")


# ============================================================================
# DATASET PREVIEW
# ============================================================================
print("\n" + "=" * 70)
print("📊 DATASET PREVIEW")
print("=" * 70)

print("\n🧑 CUSTOMERS DATA (first 5 rows):")
print(customers.head())

print(f"\nCustomers Shape: {customers.shape}")
print(f"Customers Columns: {list(customers.columns)}")
print(f"Missing values in customers:")
print(customers.isnull().sum())

print("\n" + "-" * 70)

print("\n📦 ORDERS DATA (first 5 rows):")
print(orders.head())

print(f"\nOrders Shape: {orders.shape}")
print(f"Orders Columns: {list(orders.columns)}")
print(f"Missing values in orders:")
print(orders.isnull().sum())


# ============================================================================
# QUICK STATS
# ============================================================================
print("\n" + "=" * 70)
print("📈 QUICK STATISTICS")
print("=" * 70)

print(f"\n💰 Revenue Summary:")
print(f"   Total Revenue: ₹{orders['Final_Amount'].sum():,.2f}")
print(f"   Average Order Value: ₹{orders['Final_Amount'].mean():,.2f}")
print(f"   Min Order: ₹{orders['Final_Amount'].min():,.2f}")
print(f"   Max Order: ₹{orders['Final_Amount'].max():,.2f}")

print(f"\n📊 Category Breakdown:")
category_revenue = orders.groupby('Category')['Final_Amount'].sum().sort_values(ascending=False)
for cat, rev in category_revenue.items():
    print(f"   {cat}: ₹{rev:,.2f}")

print(f"\n⭐ Average Ratings by Category:")
avg_ratings = orders.groupby('Category')['Rating'].mean().sort_values(ascending=False)
for cat, rating in avg_ratings.items():
    print(f"   {cat}: {rating:.2f}/5.0")

print(f"\n👥 Customer Segments:")
membership_counts = customers['Membership_Type'].value_counts()
for membership, count in membership_counts.items():
    percentage = (count / len(customers)) * 100
    print(f"   {membership}: {count} ({percentage:.1f}%)")

print("\n" + "=" * 70)
print("✅ DATASET GENERATION COMPLETE!")
print("=" * 70)

print("""
🎯 NEXT STEPS:
1. Open a new Python file: kaggle_analysis.py
2. Load these CSV files
3. Perform Exploratory Data Analysis (EDA)
4. Clean the data
5. Extract insights
6. Create visualizations
7. Build comprehensive report

This is your PORTFOLIO PROJECT! 🚀
""")