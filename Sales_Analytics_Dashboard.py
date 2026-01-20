"""
Sales Analytics Dashboard - Day 12 Project
Complete visualization suite using Matplotlib and Seaborn
This is what data analysts create for business stakeholders!
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set style
sns.set_style('whitegrid')
sns.set_palette('husl')

class SalesDashboard:
    """Professional sales analytics dashboard"""
    
    def __init__(self):
        """Initialize dashboard with sample data"""
        self.data = self.generate_sample_data()
        
    def generate_sample_data(self):
        """Generate realistic sales data"""
        np.random.seed(42)
        
        # Date range: Last 6 months
        dates = pd.date_range(end=datetime.now(), periods=180, freq='D')
        
        # Products
        products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones']
        
        # Regions
        regions = ['North', 'South', 'East', 'West']
        
        # Generate data
        data = []
        for date in dates:
            for product in np.random.choice(products, size=np.random.randint(5, 15)):
                region = np.random.choice(regions)
                quantity = np.random.randint(1, 10)
                
                # Base prices
                prices = {
                    'Laptop': 1200,
                    'Mouse': 25,
                    'Keyboard': 75,
                    'Monitor': 300,
                    'Headphones': 150
                }
                
                price = prices[product]
                revenue = price * quantity
                
                data.append({
                    'Date': date,
                    'Product': product,
                    'Region': region,
                    'Quantity': quantity,
                    'Price': price,
                    'Revenue': revenue
                })
        
        df = pd.DataFrame(data)
        
        # Add calculated columns
        df['Month'] = df['Date'].dt.month_name()
        df['Week'] = df['Date'].dt.isocalendar().week
        df['Weekday'] = df['Date'].dt.day_name()
        
        return df
    
    def overview_stats(self):
        """Print key metrics"""
        print("=" * 60)
        print("📊 SALES DASHBOARD - KEY METRICS")
        print("=" * 60)
        
        total_revenue = self.data['Revenue'].sum()
        total_orders = len(self.data)
        avg_order_value = self.data['Revenue'].mean()
        total_items_sold = self.data['Quantity'].sum()
        
        print(f"\n💰 Total Revenue: ${total_revenue:,.2f}")
        print(f"📦 Total Orders: {total_orders:,}")
        print(f"💵 Average Order Value: ${avg_order_value:,.2f}")
        print(f"🛒 Total Items Sold: {total_items_sold:,}")
        
        # Top product
        top_product = self.data.groupby('Product')['Revenue'].sum().idxmax()
        top_revenue = self.data.groupby('Product')['Revenue'].sum().max()
        
        print(f"\n🏆 Top Product: {top_product} (${top_revenue:,.2f})")
        
        # Top region
        top_region = self.data.groupby('Region')['Revenue'].sum().idxmax()
        region_revenue = self.data.groupby('Region')['Revenue'].sum().max()
        
        print(f"🌍 Top Region: {top_region} (${region_revenue:,.2f})")
        print("=" * 60)
    
    def create_revenue_trend(self):
        """Chart 1: Monthly revenue trend"""
        # Aggregate by month
        monthly = self.data.groupby(self.data['Date'].dt.to_period('M'))['Revenue'].sum()
        
        plt.figure(figsize=(12, 5))
        
        # Convert Period to string for plotting
        months = [str(m) for m in monthly.index]
        
        plt.plot(months, monthly.values, marker='o', linewidth=2.5, 
                color='#2E86AB', markersize=8)
        
        plt.title('Monthly Revenue Trend', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Revenue ($)', fontsize=12)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.xticks(rotation=45)
        
        # Add value labels on points
        for i, (x, y) in enumerate(zip(months, monthly.values)):
            if i % 2 == 0:  # Label every other point to avoid clutter
                plt.text(x, y, f'${y/1000:.0f}K', 
                        ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('chart1_revenue_trend.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Chart 1 saved: chart1_revenue_trend.png")
    
    def create_product_comparison(self):
        """Chart 2: Product revenue comparison"""
        product_revenue = self.data.groupby('Product')['Revenue'].sum().sort_values(ascending=True)
        
        plt.figure(figsize=(10, 6))
        
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(product_revenue)))
        
        bars = plt.barh(product_revenue.index, product_revenue.values, color=colors)
        
        plt.title('Total Revenue by Product', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Revenue ($)', fontsize=12)
        plt.ylabel('Product', fontsize=12)
        plt.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2,
                    f'${width/1000:.0f}K',
                    ha='left', va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('chart2_product_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Chart 2 saved: chart2_product_comparison.png")
    
    def create_regional_performance(self):
        """Chart 3: Regional sales performance"""
        regional = self.data.groupby('Region')['Revenue'].sum()
        
        plt.figure(figsize=(8, 8))
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        explode = (0.05, 0.05, 0.05, 0.05)
        
        wedges, texts, autotexts = plt.pie(regional.values, 
                                           labels=regional.index,
                                           autopct='%1.1f%%',
                                           colors=colors,
                                           explode=explode,
                                           shadow=True,
                                           startangle=90)
        
        # Style percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)
        
        # Style labels
        for text in texts:
            text.set_fontsize(12)
            text.set_fontweight('bold')
        
        plt.title('Revenue Distribution by Region', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig('chart3_regional_performance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Chart 3 saved: chart3_regional_performance.png")
    
    def create_weekday_analysis(self):
        """Chart 4: Sales by day of week"""
        # Order days properly
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        weekday_sales = self.data.groupby('Weekday')['Revenue'].sum()
        weekday_sales = weekday_sales.reindex(day_order)
        
        plt.figure(figsize=(12, 6))
        
        bars = plt.bar(weekday_sales.index, weekday_sales.values, 
                      color='skyblue', edgecolor='navy', linewidth=1.5)
        
        # Highlight weekend
        bars[5].set_color('lightcoral')
        bars[6].set_color('lightcoral')
        
        plt.title('Sales Performance by Day of Week', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Day', fontsize=12)
        plt.ylabel('Revenue ($)', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height,
                    f'${height/1000:.0f}K',
                    ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('chart4_weekday_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Chart 4 saved: chart4_weekday_analysis.png")
    
    def create_product_quantity_heatmap(self):
        """Chart 5: Product sales by region (heatmap)"""
        # Pivot table: Product vs Region
        heatmap_data = self.data.pivot_table(
            values='Quantity',
            index='Product',
            columns='Region',
            aggfunc='sum'
        )
        
        plt.figure(figsize=(10, 6))
        
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd',
                   linewidths=0.5, cbar_kws={'label': 'Total Quantity'})
        
        plt.title('Product Sales Quantity by Region', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Region', fontsize=12)
        plt.ylabel('Product', fontsize=12)
        
        plt.tight_layout()
        plt.savefig('chart5_product_region_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Chart 5 saved: chart5_product_region_heatmap.png")
    
    def create_price_quantity_scatter(self):
        """Chart 6: Price vs Quantity relationship"""
        # Aggregate by product
        product_data = self.data.groupby('Product').agg({
            'Price': 'mean',
            'Quantity': 'sum'
        }).reset_index()
        
        plt.figure(figsize=(10, 6))
        
        scatter = plt.scatter(product_data['Price'], 
                            product_data['Quantity'],
                            s=500, alpha=0.6, c=range(len(product_data)),
                            cmap='viridis', edgecolors='black', linewidth=2)
        
        # Add product labels
        for idx, row in product_data.iterrows():
            plt.annotate(row['Product'], 
                        (row['Price'], row['Quantity']),
                        fontsize=11, fontweight='bold',
                        ha='center', va='center')
        
        plt.title('Price vs Total Quantity Sold', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Average Price ($)', fontsize=12)
        plt.ylabel('Total Quantity Sold', fontsize=12)
        plt.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        plt.savefig('chart6_price_quantity_scatter.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Chart 6 saved: chart6_price_quantity_scatter.png")
    
    def create_comprehensive_dashboard(self):
        """Chart 7: All-in-one dashboard (subplots)"""
        fig = plt.figure(figsize=(16, 10))
        
        # Layout: 2x3 grid
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # 1. Monthly trend
        ax1 = fig.add_subplot(gs[0, :2])
        monthly = self.data.groupby(self.data['Date'].dt.to_period('M'))['Revenue'].sum()
        months = [str(m) for m in monthly.index]
        ax1.plot(months, monthly.values, marker='o', linewidth=2, color='#2E86AB')
        ax1.set_title('Monthly Revenue Trend', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Product comparison
        ax2 = fig.add_subplot(gs[0, 2])
        product_rev = self.data.groupby('Product')['Revenue'].sum().sort_values()
        ax2.barh(product_rev.index, product_rev.values, color='skyblue')
        ax2.set_title('Product Revenue', fontweight='bold')
        ax2.set_xlabel('Revenue ($)')
        
        # 3. Regional pie
        ax3 = fig.add_subplot(gs[1, 0])
        regional = self.data.groupby('Region')['Revenue'].sum()
        ax3.pie(regional.values, labels=regional.index, autopct='%1.1f%%')
        ax3.set_title('Regional Distribution', fontweight='bold')
        
        # 4. Weekday bars
        ax4 = fig.add_subplot(gs[1, 1])
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday = self.data.groupby('Weekday')['Revenue'].sum().reindex(day_order)
        ax4.bar(range(len(weekday)), weekday.values, color='lightcoral')
        ax4.set_xticks(range(len(weekday)))
        ax4.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        ax4.set_title('Weekday Sales', fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)
        
        # 5. Top products table
        ax5 = fig.add_subplot(gs[1, 2])
        ax5.axis('off')
        top_products = self.data.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(5)
        table_data = [[f"${v/1000:.1f}K"] for v in top_products.values]
        table = ax5.table(cellText=table_data,
                         rowLabels=top_products.index,
                         colLabels=['Revenue'],
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        ax5.set_title('Top 5 Products', fontweight='bold', pad=20)
        
        fig.suptitle('📊 COMPLETE SALES ANALYTICS DASHBOARD', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        plt.savefig('chart7_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Chart 7 saved: chart7_comprehensive_dashboard.png")
    
    def run_complete_analysis(self):
        """Generate all visualizations"""
        print("\n🚀 GENERATING COMPLETE SALES DASHBOARD...\n")
        
        # Show stats
        self.overview_stats()
        
        print("\n📈 Creating visualizations...\n")
        
        # Create all charts
        self.create_revenue_trend()
        self.create_product_comparison()
        self.create_regional_performance()
        self.create_weekday_analysis()
        self.create_product_quantity_heatmap()
        self.create_price_quantity_scatter()
        self.create_comprehensive_dashboard()
        
        print("\n" + "=" * 60)
        print("✅ ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
        print("=" * 60)
        print("\n📁 Files saved:")
        print("   - chart1_revenue_trend.png")
        print("   - chart2_product_comparison.png")
        print("   - chart3_regional_performance.png")
        print("   - chart4_weekday_analysis.png")
        print("   - chart5_product_region_heatmap.png")
        print("   - chart6_price_quantity_scatter.png")
        print("   - chart7_comprehensive_dashboard.png")
        print("\n💡 These charts are ready for presentations!")


# Run the dashboard
if __name__ == "__main__":    
    dashboard = SalesDashboard()
    dashboard.run_complete_analysis()
    