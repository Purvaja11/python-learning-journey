"""
Day 14 Practice: Object-Oriented Programming Exercises
Complete these to master OOP concepts for data analytics
"""

print("=" * 70)
print("DAY 14 PRACTICE: OOP EXERCISES")
print("=" * 70)


# ============================================================================
# EXERCISE 1: Create a Product Class
# ============================================================================
print("\n📦 EXERCISE 1: Product Class")
print("-" * 70)

"""
CREATE A CLASS: Product

Requirements:
1. __init__ method with: name, price, stock
2. Method: sell(quantity) - reduces stock, returns total cost
3. Method: restock(quantity) - increases stock
4. Method: get_info() - returns product details as string
5. Method: apply_discount(percent) - reduces price
"""
# TODO: Create Product class
class Product:
    """A class to represent a product in inventory"""

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def sell(self, quantity):
        """
        Sell a quantity of this product

        Parameters:
        quanntity (int): How many to sell

        Returns: 
        float: Total cost (or None if not enough stock)
        """
        # check if we have enough stock
        if quantity > self.stock:
            print(f"❌ Not enough stock! Only {self.stock} available.")
            return None
        
        #Reduce the stock
        self.stock -= quantity
        # Reduce the total cost
        total = self.price * quantity

        print(f"✅ Sold {quantity} {self.name}(s) for ${total:,.2f}")
        print(f"   Remaining stock: {self.stock}")

        return total
    
    def restock(self, quantity):
        """
        Add more stock 

        Parameters:
        quantity (int): How many to add
        """
        self.stock += quantity
        print(f"📦 Restocked {quantity} {self.name}(s)")
        print(f"   New stock level: {self.stock}")
    
    def get_info(self):
        """
        Get product information as a string

        Returns:
        str: Product details
        """
        info = f"""
Product Information:
---------------------
Name: {self.name}
Price: ${self.price:,.2f}
Stock: {self.stock} units
Value: ${self.price * self.stock:,.2f}
"""
        return info
    
    def apply_discount(self, percent):
        """
        Apply a discount to the product price

        Parameters:
        percent (float): Dicount percentage (e.g., 10 for 10%)
        """
        if percent < 0 or percent > 100:
            print("❌ Discount must be between 0 and 100!")
            return
        
        old_price = self.price
        discount_amount = self.price * (percent / 100)
        self.price -= discount_amount

        print(f"🎉 Applied {percent}% discount to {self.name}")
        print(f"    Old price: ${old_price:,.2f}")
        print(f"    Discount:-${discount_amount:,.2f}")
        print(f"    New price: ${self.price:,.2f}")

# Test your Product class:
product = Product("Laptop", 1200, 10)
print(product.get_info())
product.sell(2)
product.restock(5)
product.apply_discount(10)
print(product.get_info())


# ============================================================================
# EXERCISE 2: BankAccount with Encapsulation
# ============================================================================
print("\n💰 EXERCISE 2: Bank Account Class")
print("-" * 70)

"""
CREATE A CLASS: BankAccount

Requirements:
1. Private attribute: __balance (use double underscore)
2. __init__: owner, initial_balance
3. Method: deposit(amount) - add money (validate > 0)
4. Method: withdraw(amount) - remove money (check sufficient funds)
5. Method: get_balance() - return current balance
6. Method: transfer(other_account, amount) - transfer to another account

YOUR CODE HERE:
"""

# TODO: Create BankAccount class
class BankAccount:
    """ A class for Bank Account"""
    def __init__(self, owner, initial_balance):
        self.owner = owner
        self.__balance = initial_balance   # <- Private 
    
    def get_balance(self):
        return self.__balance   # <- Access private attribute
    
    def deposit(self, amount):
        if amount <= 0:
            print("❌ Deposit amount must be positive!")
            return False
        
        self.__balance += amount
        print(f"✅ {self.owner} deposited ${amount}")
        print(f"    New Balance: ${self.__balance:,.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Withdrawal amount must be positive!")
            return False
        
        if amount > self.__balance:
            print(f"❌ Insufficient Bank Balance. Balance ${self.__balance:,.2f}")
            return False
        
        self.__balance -= amount
        print(f"Withdrawal of ${amount:,.2f} by {self.owner}")
        print(f"New Bank Balance: ${self.__balance:,.2f}")
        return True
    
    def transfer(self, other_account, amount):
        """
        Transfer money to another account

        Parameters:
        ------------
        other_Account : BankAccount
            The account to transfer TO
        amount : float
            Amount to transfer
        """
        # Validate amount
        if amount <= 0:
            print("❌ Tranfer amount must be positive!")
            return False
        
        # Check if we have enough balance
        if amount > self.__balance:
            print(f"❌ Transfer failed! Insufficient funds.")
            print(f"   Your balance: ${self.__balance:,.2f}")
            print(f"   Transfer amount: ${amount:,.2f}")
            return False
        
        # Withdraw from this account
        self.__balance -= amount

        # Deposit to other account
        other_account.__balance += amount

        # Confirmation message
        print(f"💸 Transfer Successful!")
        print(f"    From: {self.owner} -> To: {other_account.owner}")
        print(f"    Amount: ${amount:,.2f}")
        print(f"    {self.owner}'s new balance: ${self.__balance:,.2f}")
        print(f"    {other_account.owner}'s new balance: ${other_account.__balance:,.2f}")
        return True

    

# Test your BankAccount:
account1 = BankAccount("Alice", 1000)
account2 = BankAccount("Bob", 500)
# 
account1.deposit(200)
account1.withdraw(150)
account1.transfer(account2, 300)
# 
print(f"Alice balance: ${account1.get_balance()}")
print(f"Bob balance: ${account2.get_balance()}")


# ============================================================================
# EXERCISE 3: Inheritance - Employee System
# ============================================================================
print("\n👔 EXERCISE 3: Employee Inheritance")
print("-" * 70)

"""
CREATE CLASSES WITH INHERITANCE:

1. BASE CLASS: Employee
   - Attributes: name, salary, employee_id
   - Method: get_details()
   - Method: give_raise(amount)

2. DERIVED CLASS: Manager (inherits from Employee)
   - Additional attribute: team (list of employees)
   - Method: add_team_member(employee)
   - Method: get_team_size()

3. DERIVED CLASS: Developer (inherits from Employee)
   - Additional attribute: programming_languages (list)
   - Method: add_language(language)
   - Method: get_languages()

YOUR CODE HERE:
"""

# TODO: Create Employee class
class Employee:
    """A class for Employee inheritance"""
    def __init__(self, name, salary, employee_id):
        """
        Initialize an employee
        
        Parameters:
        -----------
        name : str
            Employee name
        salary : float
            Annual salary
        employee_id : str
            Unique employee ID (e.g., "E001")
        """
        self.name = name
        self.salary = salary
        self.employee_id = employee_id
        print(f"✅ Employee created: {name} ({employee_id})")

    def get_details(self):
        """
        Get employee information as a string

        Returns:
        str: employee details
        """
        details = f"""
Product Information:
---------------------
Name: {self.name}
ID: {self.employee_id}
Salary: ${self.salary:,.2f}/year
"""
        return details
    
    def give_raise(self, amount):
        """
        Give employee a salary raise

        Parameters:
        ------------
        amount (float) : raise amount
        """
        if amount <= 0:
            print("❌ Raise amount must be positive")

        old_salary = self.salary
        self.salary += amount

        print(f"🎉 {self.name} got a raise!")
        print(f"    Old salary: ${old_salary:,.2f}")
        print(f"    Raise: +${amount:,.2f}")
        print(f"    New salary: ${self.salary:,.2f}")
    
# TODO: Create Manager class (inherits from Employee)
class Manager(Employee):
    """
    Managerclass - inherits from Employee
    Adds team management functionality
    """

    def __init__(self, name, salary, employee_id):
        """
        Initialize a manager

        Uses super() to call parent's __init__
        Then adds manager-specific attributes
        """
        # Call parent class __init__
        super().__init__(name, salary, employee_id)

        # Add manager-specific attribute
        self.team = []
        print(f"    -> Manager role assigned")

    def add_team_member(self, employee):
        """
        Add an employee to this manager's team

        Parameters:
        ------------
        employee : Employee
                Employee object to add tpo team
        """
        # Validation: check if it's an Employee
        if not isinstance(employee, Employee):
            print("❌ Can only add Employee objects to team!")
            return
        
        # Validation: don't add yourself
        if employee == self:
            print("❌ Manager cannot add themselves to their own team!")
            return
        
        # Validation: check if already in team
        if employee in self.team:
            print(f"ℹ️ {employee.name} is already in the team!")
            return
        
        # Add to team
        self.team.append(employee)
        print(f"✅ Added {employee.name} to {self.name}'s team")

    def get_team_size(self):
        """
        Get the number of team members

        Returns:
        ---------
        int
            Number of employees in team
        """
        return len(self.team)
    
    def get_details(self):
        """
        Override parent's get_details to include team info
        """
        # Get basic details from parent class
        basic_info = super().get_details()

        # Add manager-specific info
        team_info = f"""Team Size: {len(self.team)} members """

        if self.team:
            team_info += "Team Members:\n"
            for member in self.team:
                team_info += f" - {member.name} ({member.employee_id})\n"

        return basic_info + team_info



# TODO: Create Developer class (inherits from Employee)
class Developer(Employee):
    """
    Developer class - inherits from Employee
    Adds programming language management
    """
    def __init__(self, name, salary, employee_id, programming_languages=None):
        """
        Initialize a developer

        Parameters:
        -----------
        name : str
            Developer name
        salary : float
            annual salary
        employee_id : str
            Employee ID
        programming_languages : list, optional
            List of programming languages (default: empty list)
        """
        # Call parent class __init__
        super().__init__(name, salary, employee_id)

        # Add developer-specific attribute
        if programming_languages is None:
            self.programming_languages = []
        else:
            self.programming_languages = programming_languages

        print(f"    -> Developer role assigned")

    def add_language(self, language):
        """
        Add a programming language to developer's skills

        Parameters:
        -------------
        language : str
            Programming language name
        """
        # Validation: check if already known
        if language in self.programming_languages:
            print(f"ℹ️ {self.name} already knows {language}!")
            return
        
        # Add language
        self.programming_languages.append(language)
        print(f"✅ {self.name} learned {language}!")
        print(f"    Total languages: {len(self.programming_languages)}")

    def get_languages(self):
        """
        Get list of programming languages

        Returns:
        --------
        list
            List of programming language names
        """
        return self.programming_languages.copy()  #returns a copy
    
    def get_details(self):
        """
        Override parent's get_details to include languages
        """
        # Get basic details from parent class
        basic_info =  super().get_details()

        # Add developer-specific info
        lang_count = len(self.programming_languages)
        lang_info = f"""Programming Languages: {lang_count} language(s)"""

        if self.programming_languages:
            lang_info += "Skills:\n"
            for lang in self.programming_languages:
                lang_info += f" ' {lang}\n"

        return basic_info + lang_info

# Test your classes:
emp1 = Employee("John", 50000, "E001")
mgr = Manager("Sarah", 80000, "M001")
dev = Developer("Mike", 70000, "D001", ["Python", "JavaScript"])
# 
mgr.add_team_member(emp1)
mgr.add_team_member(dev)
# 
dev.add_language("SQL")
# 
print(emp1.get_details())
print(mgr.get_details())
print(f"Team size: {mgr.get_team_size()}")
print(f"Languages: {dev.get_languages()}")


# ============================================================================
# EXERCISE 4: DataProcessor Class (Data Analytics Focus)
# ============================================================================
print("\n📊 EXERCISE 4: Data Processor Class")
print("-" * 70)

"""
CREATE A CLASS: DataProcessor

This class should handle common data processing tasks.

Requirements:
1. __init__: takes a list of numbers
2. Method: get_mean() - calculate average
3. Method: get_median() - calculate median
4. Method: get_mode() - find most common value
5. Method: get_range() - max - min
6. Method: remove_outliers() - remove values > 2 std devs from mean
7. Method: get_summary() - return dictionary with all stats

YOUR CODE HERE:
"""

# TODO: Create DataProcessor class
class DataProcessor:
    """
    Process and analyze numerical data
    """
    def __init__(self, data):
        """
        Initialize with a list of numbers

        Parameters:
        -----------
        data : list
            List of numbers to analyze
        """
        # Validation
        if not data:
            raise ValueError("Data cannot be empty!")
        
        # Store data (make a copy)
        self.data = list(data)

        # Pre-calculate useful values
        self.count = len(data)

        print(f"✅ DataProcessor initialized with {self.count} values")

    def get_mean(self):
        """Calculate and return the mean (average)"""

        return sum(self.data) / self.count
    
    def get_median(self):
        """Calculate and return the median (middle value)"""
        sorted_data = sorted(self.data)
        mid = self.count // 2 

        if self.count % 2 == 0:
            # Even number: average of two middle values
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            # Odd number: middle value
            return sorted_data[mid]
        
    def get_mode(self):
        """Find and return the mode (most common value)"""
        from collections import Counter
        counts = Counter(self.data)
        max_count = max(counts.values())
        # Returns value(s) withhighest count
        return [k for k, v in counts.items() if v == max_count][0]

    def get_range(self):
        """Calculate range (max - min)"""
        max_num = max(self.data)
        min_num = min(self.data)

        return f" Range: {min_num} - {max_num}"

    def remove_outliers(self):
        """Remove values more than 2 std devs from mean"""
        mean = self.get_mean()

        # Variance
        variance = sum((x - mean) ** 2 for x in self.data) / self.count

        # std deviation
        std_dev = variance ** 0.5

        # keep values within 2 std dev
        filtered_data = [x for x in self.data if abs(x- mean) <= 2 * std_dev]

        removed = len(self.data) - len(filtered_data)

        # update data and count
        self.data = filtered_data
        self.count = len(self.data)

        print(f"\n Removed {removed} outlier(s)")
        return self.data


    def get_summary(self):
        """Return dictionary with all statistics"""
        print(" All Statistics")
        print(f" Length of data: {self.count}")
        print(f" Mean: {self.get_mean()}")
        print(f" Median: {self.get_median()}")
        print(f" Minimun value: {min(self.data)}")
        print(f" Maximum Value: {max(self.data)}")
        print(f" Most Common value: {self.get_mode()}")
        print(f" Range: {self.get_range()}")



# Test your DataProcessor:
data = [10, 20, 20, 30, 40, 50, 100, 20, 30, 25]
processor = DataProcessor(data)
# 
print(f"Mean: {processor.get_mean()}")
print(f"Median: {processor.get_median()}")
print(f"Mode: {processor.get_mode()}")
print(f"Range: {processor.get_range()}")
print("\nSummary:")
processor.get_summary()
#
processor.remove_outliers()
print("\nAfter removing outliers:")
processor.get_summary()


# ============================================================================
# EXERCISE 5: CSV Analyzer Class (Real-World Application)
# ============================================================================
print("\n📁 EXERCISE 5: CSV Analyzer Class")
print("-" * 70)

"""
CREATE A CLASS: CSVAnalyzer

This should be able to load and analyze CSV files.

Requirements:
1. __init__: takes filename
2. Method: load() - load CSV using pandas
3. Method: get_shape() - return (rows, columns)
4. Method: get_column_names() - return list of column names
5. Method: get_numeric_columns() - return list of numeric column names
6. Method: get_missing_count() - return dict of missing values per column
7. Method: get_column_stats(column_name) - return stats for that column

Bonus:
8. Method: export_summary(output_file) - save summary to CSV

YOUR CODE HERE:
"""

import pandas as pd

# TODO: Create CSVAnalyzer class
class CSVAnalyzer:
    """
    class to load and analyze CSV files
    """

    def __init__(self, data_file, name="Dataset"):
        """
        Initialize the analyzer 

        Parameters:
        -----------
        data_file : str
            Path to CSV file
        name : str
            Name for this dataset
        """
        self.name = name
        self.file_path = data_file
        self.df = None
        self.cleaned = False

        print(f"\n📊 Initializing {self.name} Analyzer...")
    
    def load(self):
        """Load data fom CSV file"""
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"✅ Loaded {len(self.df):,} records")
            
        except FileNotFoundError:
            print(f"❌ File not found: {self.file_path}")
        except Exception as e:
            print(f"❌ Error loading data: {e}")

    def get_shape(self):
        return f"{self.df.shape[0]:,} rows x {self.df.shape[1]} columns"
    
    def get_column_names(self):
        return f"{list(self.df.columns)}"
    
    def get_numeric_columns(self):
        return self.df.select_dtypes(include=['number']).columns.to_list()
    
    def get_missing_count(self):
        """Get summary of missing values"""
        if self.df is None:
            return None
        
        missing = self.df.isnull().sum()
        total = len(self.df)

        summary = pd.DataFrame({
            'Missing_Count': missing
        })

        return summary[summary['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
    
    def get_column_stats(self, column_name):
        """ Get Column stats"""
        # column exist check
        if column_name not in self.df.columns:
            raise ValueError(f"❌ Column '{column_name}' not found in CSV")
        
        col = self.df[column_name]

        # numeric check
        if not pd.api.types.is_numeric_dtype(col):
            raise TypeError(f"❌ Column '{column_name}' is not numeric")
        
        # drop missing values
        col = col.dropna()

        stats = {
            "column": column_name,
            "count": int(col.count()),
            "mean": float(col.mean()),
            "median": float(col.median()),
            "mode": float(col.mode().iloc[0]) if not col.mode().empty else None,
            "min": float(col.min()),
            "max": float(col.max()),
            "range": float(col.max() - col.min()),
            "std_dev": float(col.std())  #sample std dev
        }

        return stats
    
    def export_summary(self, output_file='summary_report.txt'):
        """Save summary to CSV file"""
        numeric_cols = self.get_numeric_columns()

        summary_list = []
        for col in numeric_cols:
            summary_list.append(self.get_column_stats(col))

        summary_df = pd.DataFrame(summary_list)

        summary_df.to_csv(output_file, index=False)
        print(f"✅ Summary exported to: {output_file}")


# Test with your e-commerce data:
analyzer = CSVAnalyzer('ecommerce_orders.csv')
analyzer.load()
# 
print(f"\nShape: {analyzer.get_shape()}")
print(f"\nColumns: {analyzer.get_column_names()}")
print(f"\nNumeric columns: {analyzer.get_numeric_columns()}")
print("\nMissing values:")
print(analyzer.get_missing_count())
print("\nStats for Final_Amount:")
print(analyzer.get_column_stats('Final_Amount'))
analyzer.export_summary()


# ============================================================================
# EXERCISE 6: Shopping Cart Class
# ============================================================================
print("\n🛒 EXERCISE 6: Shopping Cart Class")
print("-" * 70)

"""
CREATE A CLASS: ShoppingCart

Requirements:
1. __init__: empty cart (items as list of dicts)
2. Method: add_item(name, price, quantity)
3. Method: remove_item(name)
4. Method: update_quantity(name, new_quantity)
5. Method: get_total() - calculate total cost
6. Method: apply_coupon(discount_percent) - apply discount to total
7. Method: checkout() - print receipt and clear cart

YOUR CODE HERE:
"""

# TODO: Create ShoppingCart class
class ShoppingCart:
    """A class for Shopping cart"""
    def __init__(self):
        # empty cart: list of dicts
        self.items = []

    def add_item(self, name, price, quantity):
        item = {
            "name": name,
            "price": price,
            "quantity": quantity
        }
        self.items.append(item)
        print(f"✅ Added: {name} (x{quantity})")

    def remove_item(self, name):
        for item in self.items:
            if item["name"] == name:
                self.items.remove(item)
                print(f"🗑️ Removed: {name}")
                return
        
        print(f"❌ Item '{name}' not found in cart")

    def update_quantity(self, name, new_quantity):
        for item in self.items:
            if item["name"] == name:
                if new_quantity <= 0:
                    # quantity cannot be 0 or negative 
                    self.items.remove(item)
                    print(f"🗑️ Removed '{name}' because quantity became {new_quantity}")
                else:
                    item["quantity"] = new_quantity
                    print(f"🔁 Updated '{name}' quantity to {new_quantity}")
                return
        print(f"❌ Item'{name}' not found in cart")

    def get_total(self):
        return sum(item["price"] * item["quantity"] for item in self.items)
    
    def apply_coupon(self, discount_percent):
        total = self.get_total()

        if discount_percent < 0 or discount_percent > 100:
            print("❌ Discount must be between 0 and 100!")
            return
        
        discount_amount = (discount_percent / 100) * total
        final_total = total - discount_amount

        print(f"🏷️ Coupon Applied: {discount_percent}% OFF")
        print(f"💰 Total: {total}")
        print(f"🔻 Discount: {discount_amount}")
        print(f"✅ Final Total: {final_total}")

        return final_total
    
    def checkout(self):
        if not self.items:
            print("🛒 Cart is empty! Nothing to checkout.")
            return
        
        print("\n========== 🧾 RECEIPT ==========")
        for item in self.items:
            name = item["name"]
            price = item["price"]
            quantity = item["quantity"]
            line_total = price * quantity
            print(f"{name} | ₹{price} x {quantity} = ₹{line_total}")

        total = self.get_total()
        print("--------------------------------")
        print(f"TOTAL: ₹{total}")
        print("================================")

        # clear cart 
        self.items.clear()
        print("✅ Checkout complete. Cart cleared!")


    

# Test your ShoppingCart:
cart = ShoppingCart()
cart.add_item("Laptop", 1200, 1)
cart.add_item("Mouse", 25, 2)
cart.add_item("Keyboard", 75, 1)
# 
print(f"Total: ${cart.get_total()}")
cart.apply_coupon(10)
cart.checkout()


# ============================================================================
# CHALLENGE EXERCISE: Time Series Analyzer
# ============================================================================
print("\n🎯 CHALLENGE: Time Series Analyzer")
print("-" * 70)

"""
CREATE AN ADVANCED CLASS: TimeSeriesAnalyzer

This should inherit from DataAnalyzer (from the main project)
and add time-series specific functionality.

Requirements:
1. Inherit from a base analyzer class
2. Method: detect_trend() - upward, downward, or flat
3. Method: calculate_moving_average(window)
4. Method: find_peaks_and_valleys()
5. Method: forecast_next_value() - simple prediction
6. Method: plot_with_trend()

YOUR CODE HERE:
"""
from Day14_OOP_analytics_pipeline import DataAnalyzer

import matplotlib.pyplot as plt

# TODO: Create TimeSeriesAnalyzer class
# Hint: You might need to refer back to the main OOP project
class TimeSeriesAnalyzer(DataAnalyzer):
    """
    TimeSeriesAnalyzer inherits from DataAnalyzer
    and adds time-series specific analysis.
    """

    def __init__(self, data_file, time_column, value_column , name="Time Series"):
        self.time_column = time_column
        self.value_column = value_column
        super().__init__(data_file, name)

        # prepare series after loading
        self._prepare_series()

    def _prepare_series(self):
        """Prepare time series: sort by time and keep clean numeric series"""
        if self.df is None:
            raise ValueError("❌ No dataframe loaded!")
        
        if self.time_column not in self.df.columns:
            raise ValueError(f"❌ Time column '{self.time_column}' not found!")
        
        if self.value_column not in self.df.columns:
            raise ValueError(f"❌ Value column '{self.value_column}' not found!")
        
        # convert time column to datetime
        self.df[self.time_column] = pd.to_datetime(self.df[self.time_column], errors="coerce")

        # convert value column to numeric
        self.df[self.value_column] = pd.to_numeric(self.df[self.value_column], errors="coerce")

        # drop missing
        self.df = self.df.dropna(subset=[self.time_column, self.value_column])

        #sort by time
        self.df = self.df.sort_values(by=self.time_column)

        #store as series
        self.series = self.df.set_index(self.time_column)[self.value_column]

        print(f"✅ Time series prepared: {len(self.series)} points")

    #2) detect_trend
    def detect_trend(self):
        """
        Detect trend: upward, downward, flat
        based on first and last values.
        """
        if len(self.series) < 2:
            return "flat"
        
        first = self.series.iloc[0]
        last = self.series.iloc[-1]

        if last > first:
            return "upward"
        elif last < first:
            return "downward"
        return "flat"
    
    def calculate_moving_average(self, window):
        """
        Moving average using rolling window.
        Returns pandas Series.
        """
        if window <= 0:
            raise ValueError("Window must be > 0")
        
        return self.series.rolling(window=window).mean()
    
    def find_peaks_and_valleys(self):
        """
        Find peaks and valleys based on neighbor comparison.
        Returns:
            peaks: list of timestamps
            valleys: list of timestamps
        """
        values = self.series.values
        index = self.series.index

        peaks = []
        valleys = []

        for i in range(1, len(values) - 1):
            if values[i] > values[i-1] and values[i] > values[i+1]:
                peaks.append(index[i])
            elif values[i] < values[i-1] and values[i] < values[i+1]:
                valleys.append(index[i])

        return peaks, valleys
    
    def forecast_next_value(self):
        """
        Simple forecast using average change (mean delta).
        """
        if len(self.series) < 2:
            return None
        
        diffs = self.series.diff().dropna()
        avg_diff = diffs.mean()

        forecast = self.series.iloc[-1] + avg_diff
        return float(forecast)
    
    def plot_with_trend(self):
        """
        Plot time series + moving average + peaks/valleys + trend line.
        """
        if len(self.series) == 0:
            print(" No data to plot!")
            return
        
        trend = self.detect_trend()

        # trend line (endpoint linear)
        x = range(len(self.series))
        y0 = self.series.iloc[0]
        y1 = self.series.iloc[-1]
        if len(self.series) > 1:
            trend_line = [y0 + (y1 - y0) * (i / (len(self.series)-1)) for i in x]
        else:
            trend_line = [y0]

        peaks, valleys = self.find_peaks_and_valleys()

        plt.figure(figsize=(20,10))
        plt.plot(self.series.index, self.series.values, 
                 marker="o", label="Time Series", 
                 linewidth=1.5, markersize=4, alpha=0.7)

        # plot trend line
        plt.plot(self.series.index, trend_line, 
                 linestyle="--", label=f"Trend: {trend}",
                 linewidth=2, color='blue')

        # plot peaks & valleys
        if peaks:
            # Get values for peaks, handling duplicates
            peak_values = []
            for peak in peaks:
                val = self.series.loc[peak]
                if isinstance(val, pd.Series):
                    val = val.iloc[0]
                peak_values.append(float(val))
            
            plt.scatter(peaks, peak_values, color='red', s=100, 
                    label=f"Peaks ({len(peaks)})", zorder=5, marker='^', 
                    edgecolors='darkred', linewidths=2)
        if valleys:
            # Get values for valleys, handling duplicates
            valley_values = []
            for valley in valleys:
                val = self.series.loc[valley]
                if isinstance(val, pd.Series):
                    val = val.iloc[0]
                valley_values.append(float(val))
            
            plt.scatter(valleys, valley_values, color='green', s=100,
                    label=f"Valleys ({len(valleys)})", zorder=5, marker='v',
                    edgecolors='darkgreen', linewidths=2)

        plt.title(f"{self.name} - Time Series Analysis with Trend Detection", 
                  fontsize=16, fontweight='bold', pad=20)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel(self.value_column, fontsize=12)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.legend(loc='best', fontsize=10)
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig('Time_series_trend.png', dpi=300, bbox_inches='tight')
        plt.show()

        print("✅ Saved: Time_series_trend.png")


# ============================================================================
# TEST CHALLENGE: Time Series Analyzer
# ============================================================================
print("\n" + "=" * 70)
print("🎯 TESTING CHALLENGE: TIME SERIES ANALYZER")
print("=" * 70)

print("\n📊 Creating TimeSeriesAnalyzer for E-commerce Sales Data...")

# Create the analyzer with your e-commerce data
ts_analyzer = TimeSeriesAnalyzer(
    data_file='ecommerce_orders.csv',
    time_column='Order_Date',
    value_column='Final_Amount',
    name='E-commerce Daily Sales'
)

print("\n" + "-" * 70)
print("TEST 1: Basic Information")
print("-" * 70)
ts_analyzer.get_info()

print("\n" + "-" * 70)
print("TEST 2: Trend Detection")
print("-" * 70)
trend = ts_analyzer.detect_trend()
print(f"📈 Overall Sales Trend: {trend.upper()}")
print(f"   First value: ₹{ts_analyzer.series.iloc[0]:,.2f}")
print(f"   Last value: ₹{ts_analyzer.series.iloc[-1]:,.2f}")

if trend == "upward":
    print("   ✅ Sales are growing!")
elif trend == "downward":
    print("   ⚠️  Sales are declining")
else:
    print("   ➡️  Sales are stable")

print("\n" + "-" * 70)
print("TEST 3: Moving Averages")
print("-" * 70)

# Calculate different moving averages
ma_3 = ts_analyzer.calculate_moving_average(window=3)
ma_7 = ts_analyzer.calculate_moving_average(window=7)
ma_30 = ts_analyzer.calculate_moving_average(window=30)

print(f"📊 Moving Average Analysis:")
print(f"   3-day MA: {len(ma_3.dropna())} points calculated")
print(f"   7-day MA: {len(ma_7.dropna())} points calculated")
print(f"   30-day MA: {len(ma_30.dropna())} points calculated")

# Show recent moving averages
print(f"\n   Latest values:")
print(f"   Actual (last): ₹{ts_analyzer.series.iloc[-1]:,.2f}")
if not ma_7.dropna().empty:
    print(f"   7-day MA (last): ₹{ma_7.dropna().iloc[-1]:,.2f}")
if not ma_30.dropna().empty:
    print(f"   30-day MA (last): ₹{ma_30.dropna().iloc[-1]:,.2f}")

print("\n" + "-" * 70)
print("TEST 4: Peaks and Valleys Detection")
print("-" * 70)

peaks, valleys = ts_analyzer.find_peaks_and_valleys()

print(f"⛰️  Peak and Valley Analysis:")
print(f"   Total peaks found: {len(peaks)}")
print(f"   Total valleys found: {len(valleys)}")

if peaks:
    print(f"\n   📈 Peak Dates:")
    for i, peak in enumerate(peaks[:5], 1):
        peak_value = ts_analyzer.series.loc[peak]
        if isinstance(peak_value, pd.Series):
            peak_value = peak_value.iloc[0]
        peak_value = float(peak_value)
        print(f"      {i}. {peak.date()}: ₹{peak_value:,.2f}")
    if len(peaks) > 5:
        print(f"      ... and {len(peaks) - 5} more")

if valleys:
    print(f"\n   📉 Valley Dates:")
    for i, valley in enumerate(valleys[:5], 1):
        valley_value = ts_analyzer.series.loc[valley]
        if isinstance(valley_value, pd.Series):
            valley_value = valley_value.iloc[0]
        valley_value = float(valley_value)
        print(f"      {i}. {valley.date()}: ₹{valley_value:,.2f}")
    if len(valleys) > 5:
        print(f"      ... and {len(valleys) - 5} more")

print("\n" + "-" * 70)
print("TEST 5: Forecasting")
print("-" * 70)

forecast = ts_analyzer.forecast_next_value()

print(f"🔮 Sales Forecast:")
print(f"   Current (last known): ₹{ts_analyzer.series.iloc[-1]:,.2f}")
print(f"   Predicted next: ₹{forecast:,.2f}")

difference = forecast - ts_analyzer.series.iloc[-1]
percent_change = (difference / ts_analyzer.series.iloc[-1]) * 100

print(f"   Expected change: ₹{difference:,.2f} ({percent_change:+.2f}%)")

if difference > 0:
    print(f"   ✅ Forecast shows growth")
else:
    print(f"   ⚠️  Forecast shows decline")

print("\n" + "-" * 70)
print("TEST 6: Time Series Statistics")
print("-" * 70)

print(f"📊 Statistical Summary:")
print(f"   Data points: {len(ts_analyzer.series):,}")
print(f"   Date range: {ts_analyzer.series.index[0].date()} to {ts_analyzer.series.index[-1].date()}")
print(f"   Mean value: ₹{ts_analyzer.series.mean():,.2f}")
print(f"   Median value: ₹{ts_analyzer.series.median():,.2f}")
print(f"   Min value: ₹{ts_analyzer.series.min():,.2f}")
print(f"   Max value: ₹{ts_analyzer.series.max():,.2f}")
print(f"   Std deviation: ₹{ts_analyzer.series.std():,.2f}")

print("\n" + "-" * 70)
print("TEST 7: Visualization")
print("-" * 70)

print("📈 Generating time series plot with trend analysis...")
ts_analyzer.plot_with_trend()

print("\n" + "=" * 70)
print("✅ TIME SERIES ANALYZER CHALLENGE COMPLETE!")
print("=" * 70)

print("""
🎓 ADVANCED CONCEPTS DEMONSTRATED:

1. INHERITANCE IN ACTION:
   ✓ TimeSeriesAnalyzer inherits from DataAnalyzer
   ✓ Uses parent's load_data() method
   ✓ Extends with time-series specific methods
   ✓ Demonstrates code reuse through inheritance

2. TIME SERIES ANALYSIS:
   ✓ Trend detection (upward/downward/flat)
   ✓ Moving average calculations
   ✓ Peak and valley identification
   ✓ Simple forecasting algorithm
   ✓ Data visualization

3. DATA PREPARATION:
   ✓ Date/time conversion
   ✓ Data type validation
   ✓ Sorting by timestamp
   ✓ Missing data handling
   ✓ Series creation from DataFrame

4. STATISTICAL METHODS:
   ✓ Rolling window calculations
   ✓ Neighbor comparison algorithms
   ✓ Delta-based forecasting
   ✓ Summary statistics

💼 REAL-WORLD APPLICATIONS:
   • Stock price analysis
   • Sales trend monitoring
   • Website traffic analysis
   • IoT sensor data
   • Financial forecasting

🎯 INTERVIEW TALKING POINTS:
"I built a TimeSeriesAnalyzer that inherits from a base DataAnalyzer
class. It demonstrates inheritance by reusing the parent's data loading
functionality while adding specialized time-series methods like trend
detection, moving averages, and forecasting. The class handles real-world
challenges like date conversion, data sorting, and missing values. I also
implemented peak/valley detection using neighbor comparison and created
visualizations to present findings clearly."
""")

# ============================================================================
# COMPLETION CHECKLIST
# ============================================================================
print("\n" + "=" * 70)
print("✅ COMPLETION CHECKLIST")
print("=" * 70)
print("""
□ Exercise 1: Product Class (basic OOP)
□ Exercise 2: BankAccount (encapsulation)
□ Exercise 3: Employee System (inheritance)
□ Exercise 4: DataProcessor (data analytics)
□ Exercise 5: CSVAnalyzer (real-world application)
□ Exercise 6: ShoppingCart (practical example)
□ Challenge: TimeSeriesAnalyzer (advanced)

💡 LEARNING GOALS:
✓ Understand class creation and __init__
✓ Master instance methods and self
✓ Practice encapsulation (private attributes)
✓ Implement inheritance effectively
✓ Apply OOP to data analytics problems

🎯 INTERVIEW PREPARATION:
When asked "Explain OOP":
1. Classes = Blueprints for objects
2. Objects = Instances created from classes
3. Inheritance = Code reuse through parent classes
4. Encapsulation = Data protection with private attributes
5. Real example: "I built a DataAnalyzer class hierarchy..."

💼 REAL-WORLD RELEVANCE:
- NetWeb uses OOP for enterprise software
- Data pipelines are built with classes
- Reusable analytics tools use OOP
- Team projects require organized code

🚀 NEXT STEPS:
After completing exercises:
1. Run the main OOP analytics project
2. Try extending it with new methods
3. Create your own analyzer class
4. Practice explaining OOP concepts aloud
""")