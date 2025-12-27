print("="*50)
print("SHOPPING LIST MANAGER")
print("="*50)

products = ["Apple", "Banana", "Orange", "Milk", "Bread"]
prices = [1.50, 0.75, 2.00, 3.50, 2.50]

print("\nAvailable Products:")
for i,(product,price) in enumerate(zip(products, prices)):
    print(f"{i+1}.{product} - ${price:.2f}")

#TOTAL COST
total_cost = sum(prices)
print(f"\nTotal cost of all products: {total_cost:.2f}")

#MOST EXPENSIVE & CHEAPEST
max_price = max(prices)
min_price = min(prices)
max_index = prices.index(max_price)
min_index = prices.index(min_price)

print(f"\nMost Expensive Product: {products[max_index]} (${max_price:.2f})")
print(f"Cheapest Product: {products[max_index]} (${min_price:.2f})")

#Expensive items(price>$2.00)
expensive_items = [product for product, price in zip(products, prices) if price > 2.00]
print(f"\nExpensive Items (>$2.00): {expensive_items}")

#product names in upper case
upper_products = [product.upper() for product in products]
print(f"Products in UPPERCASE: {upper_products}")
