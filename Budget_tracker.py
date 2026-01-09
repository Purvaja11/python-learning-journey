import numpy as np
# Option A: Budget Tracker (Recommended - Easiest)

print("="*50)
print("BUDGET TRACKER")
print("="*50)

# Create this structure:
# - 12 months of data
# - 5 expense categories (Food, Transport, Rent, Entertainment, Utilities)
# - Analyze spending patterns
# - Find which months overspent
# - Calculate category averages

np.random.seed(42)
data = np.random.randint(1000, 5000, size=(12,5))
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
categories = ['Food', 'Transport', 'Rent', 'Entertainment', 'Utilities']

print(f"\nDataShape: {data.shape} (12 months, 5 categories)")
print(f"Budget limit per month: $10,000")

#Analyze spending patterns
print("\n" + "="*50)
print("\n📈 SPENDING PATTERNS")
print("="*50)

monthly_totals = np.sum(data, axis=1)
sorted_indices = np.argsort(monthly_totals)[::-1]

print("\nMonths ranked by total spending:")
print("="*50)
for rank, idx in enumerate(sorted_indices, 1):
    total = monthly_totals[idx]
    print(f"{rank:2d}. {months[idx]:8s} - ${total:,}"
          f"{'🔴 HIGH' if total > 15000 else '🟢 OK'}")

#Months overspent
print("\n" + "="*50)
print("\n BUDGET ANALYSIS (Limit: $10,000/month)")
print("="*50)

budget_limit = 10000

#Months where total spending exceeded
overspent_mask = monthly_totals > budget_limit
overspent_indices = np.where(overspent_mask)[0]

if len(overspent_indices) > 0:
    print(f"\n{len(overspent_indices)} months exceeded budget:")
    print("="*50)
    total_overspending = 0

    for idx in overspent_indices:
        spent = monthly_totals[idx]
        excess = spent - budget_limit
        total_overspending += excess
        print(f"{months[idx]:8s}: ${spent:,} (Over by ${excess:,})")

    print(f"\nTotal overspending: ${total_overspending}")
else:
    print("\nAll months within budget! Great job!")

#Category averages
print("\n" + "="*50)
print("\nCATEGORY AVERAGES:")
print("="*50)

#Average spending per category(across months)
category_averages = np.mean(data, axis=0)
category_totals = np.sum(data, axis=0)

print("\nAnnual spending by category:")
print("="*50)
for i, category in enumerate(categories):
    avg = category_averages[i]
    total = category_totals[i]
    percentage = (total / np.sum(data)) * 100
    print(f"{category:18s}: Avg: ${avg:>7,.0f}/month |"
          f"Total: ${total:>8,} ({percentage:>5.1f}%)")
    
#highest & lowest spending category
highest_cat_idx = np.argmax(category_totals)
lowest_cat_idx = np.argmin(category_totals)

print(f"\n💰 Highest: {categories[highest_cat_idx]}"
      f"(${category_totals[highest_cat_idx]:,})")
print(f"💵 Lowest: {categories[lowest_cat_idx]}"
      f"(${category_totals[lowest_cat_idx]})")

#Spending Trends
print("\n" + "="*60)
print("📉 SPENDING TRENDS")
print("="*60)

#first half vs second half
first_half = np.mean(monthly_totals[:6])
second_half = np.mean(monthly_totals[6:])
change = ((second_half - first_half) / first_half)*100

print(f"\nFirst half average (Jan-Jun): ${first_half:,.0f}")
print(f"Second half average: ${second_half:,.0f}")
print(f"Change: {change:+.1f}")

if change > 10:
    print("📈 Trend: Spending increased significantly in second half")
elif change < -10:
    print("📉 Trend: Spending decreased in second half - good savings!")
else:
    print("➡️ Trend: Spending remained relatively stable")


#Detailed Monthly breakdown
print("\n" + "="*60)
print("📋 DETAILED MONTHLY BREAKDOWN")
print("="*60)

for i, month in enumerate(months):
    total = monthly_totals[i]
    print(f"\n{month} - Total: ${total:,}")
    print("="*60)
    for j, category in enumerate(categories):
        amount = data[i, j]
        percentage = (amount / total) * 100
        print(f" {category}: ${amount:>6,} ({percentage:>5.1f}%)")


#Summamry statistics
print("\n" + "="*60)
print("📊 ANNUAL SUMMARY")
print("="*60)

total_annual = np.sum(data)
avg_monthly = np.mean(monthly_totals)
max_month = np.max(monthly_totals)
min_month = np.min(monthly_totals)
std_dev = np.std(monthly_totals)

print(f"\nTotal Annual Spending: ${total_annual:,}")
print(f"Average Monthly:       ${avg_monthly:,.0f}")
print(f"Highest Month:         ${max_month:,} ({months[np.argmax(monthly_totals)]})")
print(f"Lowest Month:          ${min_month:,} ({months[np.argmin(monthly_totals)]})")
print(f"Standard Deviation:    ${std_dev:,.0f}")
print(f"Budget Adherence:      {(12 - len(overspent_indices))/12*100:.0f}% of months")


#Recommendations
print("\n" + "="*60)
print("💡 RECOMMENDATIONS")
print("="*60)

#Category to reduce
highest_spending_cat = categories[highest_cat_idx]
potential_savings = category_averages[highest_cat_idx] * 0.1 #10% reduction

print(f"\n1. Reduce: {highest_spending_cat} by 10%")
print(f"    Potential montly savings: ${potential_savings:,.0f}")
print(f"    Annual savings: ${potential_savings * 12:,.0f}")

#if entertainment is high
entertainment_idx = categories.index('Entertainment')
if category_averages[entertainment_idx] > 2000:
    print(f"\n2. Entertainment spending is above $2,000/month")
    print(f"    Consider cutting back on non-essential activities")

#Budget advice
if len(overspent_indices) > 6:
    print(f"\n3. ⚠️  Over 50% of months exceeded  budget")
    print(f"    Consider increasing budget limit or cutting expenses")

print("\n" + "="*60)