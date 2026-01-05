"""
Sales Data Analyzer - Day 6 Project
Demonstrates: File I/O, Exception Handling, Classes, Data Processing

This project shows real-world data analytics skills!
"""

import csv
from datetime import datetime

class SalesRecord:
    """Represents a single sales transaction"""
    
    def __init__(self, date, product, category, quantity, price):
        self.date = date
        self.product = product
        self.category = category
        self.quantity = int(quantity)
        self.price = float(price)
        self.total = self.quantity * self.price
    
    def __repr__(self):
        return f"{self.product}: {self.quantity} x ${self.price} = ${self.total:.2f}"

class SalesAnalyzer:
    """Analyzes sales data from CSV file"""
    
    def __init__(self):
        self.records = []
    
    def load_from_csv(self, filename):
        """Load sales data from CSV file"""
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    record = SalesRecord(
                        row['date'],
                        row['product'],
                        row['category'],
                        row['quantity'],
                        row['price']
                    )
                    self.records.append(record)
            print(f"✓ Loaded {len(self.records)} records from {filename}")
            return True
        except FileNotFoundError:
            print(f"✗ Error: File '{filename}' not found!")
            return False
        except KeyError as e:
            print(f"✗ Error: Missing column {e} in CSV file!")
            return False
        except ValueError as e:
            print(f"✗ Error: Invalid data format - {e}")
            return False
    
    def calculate_total_sales(self):
        """Calculate total sales revenue"""
        return sum(record.total for record in self.records)
    
    def get_sales_by_category(self):
        """Group sales by category"""
        category_sales = {}
        for record in self.records:
            if record.category not in category_sales:
                category_sales[record.category] = 0
            category_sales[record.category] += record.total
        return category_sales
    
    def get_top_products(self, n=5):
        """Get top N products by revenue"""
        product_sales = {}
        for record in self.records:
            if record.product not in product_sales:
                product_sales[record.product] = 0
            product_sales[record.product] += record.total
        
        # Sort by revenue (descending)
        sorted_products = sorted(
            product_sales.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return sorted_products[:n]
    
    def get_average_sale_value(self):
        """Calculate average transaction value"""
        if not self.records:
            return 0
        return self.calculate_total_sales() / len(self.records)
    
    def save_report(self, filename):
        """Save analysis report to file"""
        try:
            with open(filename, 'w') as file:
                file.write("="*60 + "\n")
                file.write("SALES ANALYSIS REPORT\n")
                file.write("="*60 + "\n\n")
                
                # Total sales
                total = self.calculate_total_sales()
                file.write(f"Total Sales: ${total:,.2f}\n")
                file.write(f"Total Transactions: {len(self.records)}\n")
                file.write(f"Average Sale: ${self.get_average_sale_value():.2f}\n\n")
                
                # Sales by category
                file.write("-"*60 + "\n")
                file.write("SALES BY CATEGORY\n")
                file.write("-"*60 + "\n")
                category_sales = self.get_sales_by_category()
                for category, amount in sorted(category_sales.items(), 
                                               key=lambda x: x[1], 
                                               reverse=True):
                    percentage = (amount / total) * 100
                    file.write(f"{category}: ${amount:,.2f} ({percentage:.1f}%)\n")
                
                # Top products
                file.write("\n" + "-"*60 + "\n")
                file.write("TOP 5 PRODUCTS\n")
                file.write("-"*60 + "\n")
                top_products = self.get_top_products(5)
                for i, (product, revenue) in enumerate(top_products, 1):
                    file.write(f"{i}. {product}: ${revenue:,.2f}\n")

                # Sales by Date
                file.write("\n" + "-"*60 + "\n")
                file.write("SALES BY DATE\n")
                file.write("-"*60 + "\n")
                date_sales = self.get_sales_by_date()
                for date, amount in sorted(date_sales.items(),
                                           key=lambda x: x[1],
                                           reverse=True):
                    percentage = (amount / total) * 100
                    file.write(f"{date}: ${amount:,.2f} ({percentage:.1f}%)\n")
               
                file.write("\n" + "="*60 + "\n")
                file.write(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                file.write("="*60 + "\n")
            
            print(f"✓ Report saved to {filename}")
            return True
        except Exception as e:
            print(f"✗ Error saving report: {e}")
            return False
    
    def get_sales_by_date(self):
        """Group sales by date"""
        date_sales = {}
        for record in self.records:
            if record.date not in date_sales:
                date_sales[record.date] = 0
            date_sales[record.date] += record.total
        return date_sales
    
    def find_product_by_name(self, search_term):
        """Search for products containing search term"""
        results = [r for r in self.records if search_term.lower() in r.product.lower()]
        return results

    

# Create sample CSV data if file doesn't exist
def create_sample_data(filename="sales_data.csv"):
    """Create sample sales data for testing"""
    sample_data = [
        ["date", "product", "category", "quantity", "price"],
        ["2024-01-01", "Laptop", "Electronics", "5", "899.99"],
        ["2024-01-02", "Mouse", "Electronics", "15", "25.50"],
        ["2024-01-02", "Desk Chair", "Furniture", "8", "199.99"],
        ["2024-01-03", "Monitor", "Electronics", "10", "299.99"],
        ["2024-01-03", "Desk Lamp", "Furniture", "12", "45.00"],
        ["2024-01-04", "Keyboard", "Electronics", "20", "79.99"],
        ["2024-01-04", "Notebook", "Stationery", "50", "3.99"],
        ["2024-01-05", "Pen Set", "Stationery", "30", "12.50"],
        ["2024-01-05", "Office Desk", "Furniture", "6", "349.99"],
        ["2024-01-06", "Webcam", "Electronics", "8", "89.99"],
    ]
    
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(sample_data)
        print(f"✓ Sample data created: {filename}")
        return True
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")
        return False



# Main program
def main():
    print("="*60)
    print("SALES DATA ANALYZER")
    print("="*60)
    
    # Create analyzer object
    analyzer = SalesAnalyzer()
    
    # Menu
    while True:
        print("\nMENU:")
        print("1. Load sales data from CSV")
        print("2. View total sales")
        print("3. View sales by category")
        print("4. View top products")
        print("5. Generate report")
        print("6. View sales by date")
        print("7. Search for product")
        print("8. Create sample data")
        print("9. Exit")
        
        choice = input("\nChoose option (1-9): ")
        
        if choice == "1":
            filename = input("Enter CSV filename (or press Enter for 'sales_data.csv'): ").strip()
            if not filename:
                filename = "sales_data.csv"
            analyzer.load_from_csv(filename)
        
        elif choice == "2":
            if not analyzer.records:
                print("✗ No data loaded! Load data first.")
            else:
                total = analyzer.calculate_total_sales()
                avg = analyzer.get_average_sale_value()
                print(f"\n💰 Total Sales: ${total:,.2f}")
                print(f"📊 Total Transactions: {len(analyzer.records)}")
                print(f"📈 Average Sale: ${avg:.2f}")
        
        elif choice == "3":
            if not analyzer.records:
                print("✗ No data loaded! Load data first.")
            else:
                print("\n📊 SALES BY CATEGORY:")
                print("-"*40)
                category_sales = analyzer.get_sales_by_category()
                total = analyzer.calculate_total_sales()
                for category, amount in sorted(category_sales.items(), 
                                               key=lambda x: x[1], 
                                               reverse=True):
                    percentage = (amount / total) * 100
                    print(f"{category:15} ${amount:>10,.2f} ({percentage:>5.1f}%)")
        
        elif choice == "4":
            if not analyzer.records:
                print("✗ No data loaded! Load data first.")
            else:
                print("\n🏆 TOP 5 PRODUCTS:")
                print("-"*40)
                top_products = analyzer.get_top_products(5)
                for i, (product, revenue) in enumerate(top_products, 1):
                    print(f"{i}. {product:20} ${revenue:>10,.2f}")
        
        elif choice == "5":
            if not analyzer.records:
                print("✗ No data loaded! Load data first.")
            else:
                filename = input("Enter report filename (default: 'sales_report.txt'): ").strip()
                if not filename:
                    filename = "sales_report.txt"
                analyzer.save_report(filename)
                
        elif choice == "6":
            if not analyzer.records:
                print("✗ No data loaded! Load data first.")
            else:
                print("\n📊 SALES BY DATE:")
                print("-"*40)
                date_sales = analyzer.get_sales_by_date()
                total = analyzer.calculate_total_sales()
                for date, amount in sorted(date_sales.items(),
                                           key=lambda x: x[1],
                                           reverse=True):
                    percentage = (amount / total) * 100
                    print(f"{date:15} ${amount:.2f} ({percentage:>5.1f}%)")

        elif choice == "7":
            if not analyzer.records:
                print("✗ No data loaded! Load data first.")
            else:
                search_term = input("Enter product name to search: ").strip()
                results = analyzer.find_product_by_name(search_term)
                
                if results:
                    print(f"\n🔍 SEARCH RESULTS for '{search_term}':")
                    print("-"*40)
                    total_revenue = sum(r.total for r in results)
                    total_quantity = sum(r.quantity for r in results)
                    
                    for record in results:
                        print(f"  Date: {record.date}")
                        print(f"  Product: {record.product}")
                        print(f"  Category: {record.category}")
                        print(f"  Quantity: {record.quantity}")
                        print(f"  Price: ${record.price:.2f}")
                        print(f"  Total: ${record.total:.2f}")
                        print("-"*40)
                    
                    print(f"\n📊 SUMMARY:")
                    print(f"  Total transactions: {len(results)}")
                    print(f"  Total quantity sold: {total_quantity}")
                    print(f"  Total revenue: ${total_revenue:.2f}")
                else:
                    print(f"\n✗ No products found matching '{search_term}'")       

        elif choice == "8":
            create_sample_data()
        
        elif choice == "9":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("✗ Invalid choice! Please choose 1-7.")

if __name__ == "__main__":
    main()