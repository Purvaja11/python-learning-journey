"""
Stock Price Analyzer - Day 7 Project
Demonstrates: NumPy arrays, vectorization, statistical analysis

Analyzes stock price data using NumPy
Time Complexity: O(n) for most operations
Space Complexity: O(n) for storing arrays
"""

import numpy as np

class StockAnalyzer:
    """Analyze stock price data using NumPy"""
    
    def __init__(self, prices):
        """Initialize with array of prices"""
        self.prices = np.array(prices)
        self.returns = self.calculate_returns()
    
    def calculate_returns(self):
        """Calculate daily returns (percentage change)"""
        if len(self.prices) < 2:
            return np.array([])
        # Return = (Today - Yesterday) / Yesterday * 100
        returns = (self.prices[1:] - self.prices[:-1]) / self.prices[:-1] * 100
        return returns
    
    def get_basic_stats(self):
        """Get basic price statistics"""
        return {
            'current_price': self.prices[-1],
            'min_price': np.min(self.prices),
            'max_price': np.max(self.prices),
            'avg_price': np.mean(self.prices),
            'median_price': np.median(self.prices),
            'std_dev': np.std(self.prices),
            'price_range': np.max(self.prices) - np.min(self.prices)
        }
    
    def get_return_stats(self):
        """Get return statistics"""
        if len(self.returns) == 0:
            return None
        
        return {
            'avg_return': np.mean(self.returns),
            'median_return': np.median(self.returns),
            'best_day': np.max(self.returns),
            'worst_day': np.min(self.returns),
            'volatility': np.std(self.returns),
            'positive_days': np.sum(self.returns > 0),
            'negative_days': np.sum(self.returns < 0)
        }
    
    def find_price_above(self, threshold):
        """Find all prices above threshold"""
        return self.prices[self.prices > threshold]
    
    def find_price_below(self, threshold):
        """Find all prices below threshold"""
        return self.prices[self.prices < threshold]
    
    def calculate_moving_average(self, window=5):
        """Calculate moving average"""
        if len(self.prices) < window:
            return None
        
        # Use NumPy's convolve for moving average
        weights = np.ones(window) / window
        return np.convolve(self.prices, weights, mode='valid')
    
    def detect_trend(self):
        """Detect overall trend (upward/downward/sideways)"""
        if len(self.prices) < 2:
            return "Insufficient data"
        
        # Compare first half average with second half
        mid = len(self.prices) // 2
        first_half_avg = np.mean(self.prices[:mid])
        second_half_avg = np.mean(self.prices[mid:])
        
        diff = second_half_avg - first_half_avg
        percent_change = (diff / first_half_avg) * 100
        
        if percent_change > 5:
            return "Upward Trend 📈"
        elif percent_change < -5:
            return "Downward Trend 📉"
        else:
            return "Sideways/Flat ➡️"
    
    def find_support_resistance(self):
        """Find support (low) and resistance (high) levels"""
        # Support: Average of bottom 20% prices
        # Resistance: Average of top 20% prices
        sorted_prices = np.sort(self.prices)
        n = len(sorted_prices)
        
        bottom_20 = int(n * 0.2)
        top_20 = int(n * 0.8)
        
        support = np.mean(sorted_prices[:bottom_20])
        resistance = np.mean(sorted_prices[top_20:])
        
        return {'support': support, 'resistance': resistance}
    
    def calculate_rsi(self, period=14):
        """Calculate Relative Strength Index (RSI)"""
        if len(self.returns) < period:
            return None
        
        # Separate gains and losses
        gains = np.where(self.returns > 0, self.returns, 0)
        losses = np.where(self.returns < 0, -self.returns, 0)
        
        # Average gains and losses
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def generate_signals(self):
        """Generate buy/sell signals based on analysis"""
        rsi = self.calculate_rsi()
        trend = self.detect_trend()
        stats = self.get_basic_stats()
        
        signals = []
        
        # RSI signals
        if rsi is not None:
            if rsi < 30:
                signals.append("🟢 BUY Signal: RSI indicates oversold")
            elif rsi > 70:
                signals.append("🔴 SELL Signal: RSI indicates overbought")
        
        # Trend signals
        if "Upward" in trend:
            signals.append("📈 Trend: Strong upward momentum")
        elif "Downward" in trend:
            signals.append("📉 Trend: Bearish momentum")
        
        # Price vs Moving Average
        ma = self.calculate_moving_average()
        if ma is not None and len(ma) > 0:
            current_price = stats['current_price']
            recent_ma = ma[-1]
            
            if current_price > recent_ma * 1.02:
                signals.append("💪 Price above moving average (bullish)")
            elif current_price < recent_ma * 0.98:
                signals.append("⚠️ Price below moving average (bearish)")
        
        return signals if signals else ["➡️ HOLD: No clear signals"]

# Demo function
def create_sample_data():
    """Create sample stock price data"""
    # Simulate 30 days of stock prices
    np.random.seed(42)
    base_price = 100
    daily_changes = np.random.randn(30) * 2  # Random changes
    prices = base_price + np.cumsum(daily_changes)  # Cumulative sum
    prices = np.maximum(prices, 50)  # Minimum price of 50
    return prices

# Main program
def main():
    print("="*60)
    print("STOCK PRICE ANALYZER")
    print("="*60)
    
    # Menu
    while True:
        print("\nMENU:")
        print("1. Use sample data (30 days)")
        print("2. Enter custom prices")
        print("3. Exit")
        
        choice = input("\nChoose option (1-3): ")
        
        if choice == "1":
            prices = create_sample_data()
            print(f"\n✓ Loaded {len(prices)} days of sample data")
            
        elif choice == "2":
            print("\nEnter stock prices (comma-separated):")
            print("Example: 100,102,98,105,103")
            try:
                input_str = input("Prices: ")
                prices = np.array([float(x.strip()) for x in input_str.split(",")])
                print(f"\n✓ Loaded {len(prices)} price points")
            except ValueError:
                print("✗ Invalid input! Please use numbers only.")
                continue
        
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("✗ Invalid choice!")
            continue
        
        # Create analyzer
        analyzer = StockAnalyzer(prices)
        
        # Analysis menu
        while True:
            print("\n" + "="*60)
            print("ANALYSIS MENU")
            print("="*60)
            print("1. View price statistics")
            print("2. View return statistics")
            print("3. View moving average")
            print("4. View trend analysis")
            print("5. View support/resistance levels")
            print("6. Calculate RSI")
            print("7. Generate trading signals")
            print("8. Filter prices (above/below threshold)")
            print("9. View all prices")
            print("10. Back to main menu")
            
            analysis_choice = input("\nChoose option (1-10): ")
            
            if analysis_choice == "1":
                stats = analyzer.get_basic_stats()
                print("\n📊 PRICE STATISTICS:")
                print("-"*40)
                print(f"Current Price:  ${stats['current_price']:.2f}")
                print(f"Average Price:  ${stats['avg_price']:.2f}")
                print(f"Median Price:   ${stats['median_price']:.2f}")
                print(f"Minimum Price:  ${stats['min_price']:.2f}")
                print(f"Maximum Price:  ${stats['max_price']:.2f}")
                print(f"Price Range:    ${stats['price_range']:.2f}")
                print(f"Volatility:     ${stats['std_dev']:.2f}")
            
            elif analysis_choice == "2":
                stats = analyzer.get_return_stats()
                if stats:
                    print("\n📈 RETURN STATISTICS:")
                    print("-"*40)
                    print(f"Average Return:  {stats['avg_return']:.2f}%")
                    print(f"Median Return:   {stats['median_return']:.2f}%")
                    print(f"Best Day:        {stats['best_day']:.2f}%")
                    print(f"Worst Day:       {stats['worst_day']:.2f}%")
                    print(f"Volatility:      {stats['volatility']:.2f}%")
                    print(f"Positive Days:   {stats['positive_days']}")
                    print(f"Negative Days:   {stats['negative_days']}")
                else:
                    print("✗ Not enough data for return analysis")
            
            elif analysis_choice == "3":
                ma = analyzer.calculate_moving_average()
                if ma is not None:
                    print("\n📉 5-DAY MOVING AVERAGE:")
                    print("-"*40)
                    for i, avg in enumerate(ma, 5):
                        print(f"Day {i}: ${avg:.2f}")
                else:
                    print("✗ Not enough data for moving average")
            
            elif analysis_choice == "4":
                trend = analyzer.detect_trend()
                print("\n🎯 TREND ANALYSIS:")
                print("-"*40)
                print(f"Overall Trend: {trend}")
            
            elif analysis_choice == "5":
                levels = analyzer.find_support_resistance()
                print("\n📏 SUPPORT & RESISTANCE LEVELS:")
                print("-"*40)
                print(f"Support Level:    ${levels['support']:.2f}")
                print(f"Resistance Level: ${levels['resistance']:.2f}")
            
            elif analysis_choice == "6":
                rsi = analyzer.calculate_rsi()
                if rsi is not None:
                    print("\n💹 RELATIVE STRENGTH INDEX (RSI):")
                    print("-"*40)
                    print(f"RSI Value: {rsi:.2f}")
                    if rsi < 30:
                        print("Status: OVERSOLD (possible buy opportunity)")
                    elif rsi > 70:
                        print("Status: OVERBOUGHT (possible sell opportunity)")
                    else:
                        print("Status: NEUTRAL")
                else:
                    print("✗ Not enough data for RSI calculation")
            
            elif analysis_choice == "7":
                signals = analyzer.generate_signals()
                print("\n🚦 TRADING SIGNALS:")
                print("-"*40)
                for signal in signals:
                    print(f"  {signal}")
            
            elif analysis_choice == "8":
                try:
                    threshold = float(input("\nEnter price threshold: $"))
                    above = analyzer.find_price_above(threshold)
                    below = analyzer.find_price_below(threshold)
                    
                    print(f"\n🔍 PRICE FILTER (Threshold: ${threshold:.2f}):")
                    print("-"*40)
                    print(f"Prices above: {len(above)} days")
                    if len(above) > 0:
                        print(f"  Average: ${np.mean(above):.2f}")
                    print(f"Prices below: {len(below)} days")
                    if len(below) > 0:
                        print(f"  Average: ${np.mean(below):.2f}")
                except ValueError:
                    print("✗ Invalid number!")
            
            elif analysis_choice == "9":
                print("\n📋 ALL PRICES:")
                print("-"*40)
                for i, price in enumerate(analyzer.prices, 1):
                    if i % 5 == 0:
                        print(f"Day {i}: ${price:.2f}")
                    else:
                        print(f"Day {i}: ${price:.2f}", end="  ")
                print()
            
            elif analysis_choice == "10":
                break
            
            else:
                print("✗ Invalid choice!")

if __name__ == "__main__":
    main()