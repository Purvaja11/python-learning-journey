"""
Employee Performance Analyzer - Day 8 Project
Advanced NumPy: Multi-dimensional analysis, statistical operations, data pipeline

Analyzes employee performance across multiple metrics
Time Complexity: O(n*m) where n=employees, m=metrics
Space Complexity: O(n*m)
"""

import numpy as np
import csv
from datetime import datetime

class EmployeeAnalyzer:
    """Analyze employee performance using advanced NumPy"""
    
    def __init__(self):
        self.employees = []
        self.performance_data = None
        self.metrics = ['Sales', 'Customer_Satisfaction', 'Projects_Completed', 
                       'Attendance', 'Team_Collaboration']
    
    def load_sample_data(self):
        """Generate sample employee data"""
        np.random.seed(42)
        
        names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 
                'Frank', 'Grace', 'Henry', 'Ivy', 'Jack']
        
        self.employees = names
        
        # Performance metrics (10 employees x 5 metrics)
        # Values between 60-100
        self.performance_data = np.random.randint(60, 101, size=(10, 5))
        
        print(f"✓ Loaded {len(self.employees)} employees with {len(self.metrics)} metrics")
        return True
    
    def load_from_csv(self, filename):
        """Load employee data from CSV"""
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                self.employees = []
                data_list = []
                
                for row in reader:
                    self.employees.append(row['Name'])
                    metrics = [float(row[m]) for m in self.metrics]
                    data_list.append(metrics)
                
                self.performance_data = np.array(data_list)
                print(f"✓ Loaded {len(self.employees)} employees from {filename}")
                return True
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            return False
    
    def save_to_csv(self, filename):
        """Save data to CSV"""
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                # Header
                writer.writerow(['Name'] + self.metrics)
                # Data
                for i, name in enumerate(self.employees):
                    row = [name] + list(self.performance_data[i])
                    writer.writerow(row)
            print(f"✓ Data saved to {filename}")
            return True
        except Exception as e:
            print(f"✗ Error saving: {e}")
            return False
    
    def get_overall_stats(self):
        """Calculate overall performance statistics"""
        if self.performance_data is None:
            return None
        
        return {
            'mean': np.mean(self.performance_data),
            'median': np.median(self.performance_data),
            'std': np.std(self.performance_data),
            'min': np.min(self.performance_data),
            'max': np.max(self.performance_data)
        }
    
    def get_employee_scores(self):
        """Calculate overall score for each employee (average across metrics)"""
        return np.mean(self.performance_data, axis=1)
    
    def get_metric_averages(self):
        """Calculate average for each metric (average across employees)"""
        return np.mean(self.performance_data, axis=0)
    
    def rank_employees(self):
        """Rank employees by overall performance"""
        scores = self.get_employee_scores()
        # argsort returns indices in ascending order, [::-1] reverses to descending
        ranked_indices = np.argsort(scores)[::-1]
        
        rankings = []
        for rank, idx in enumerate(ranked_indices, 1):
            rankings.append({
                'rank': rank,
                'name': self.employees[idx],
                'score': scores[idx]
            })
        return rankings
    
    def find_top_performers(self, n=3):
        """Find top N performers"""
        rankings = self.rank_employees()
        return rankings[:n]
    
    def find_underperformers(self, threshold=70):
        """Find employees with average score below threshold"""
        scores = self.get_employee_scores()
        underperforming = np.where(scores < threshold)[0]
        
        result = []
        for idx in underperforming:
            result.append({
                'name': self.employees[idx],
                'score': scores[idx],
                'gap': threshold - scores[idx]
            })
        return result
    
    def analyze_metric_correlations(self):
        """Find correlations between metrics"""
        correlation_matrix = np.corrcoef(self.performance_data.T)
        return correlation_matrix
    
    def identify_strengths_weaknesses(self, employee_idx):
        """Identify employee's strengths and weaknesses"""
        employee_scores = self.performance_data[employee_idx]
        metric_averages = self.get_metric_averages()
        
        # Compare employee to average
        differences = employee_scores - metric_averages
        
        strengths = []
        weaknesses = []
        
        for i, diff in enumerate(differences):
            if diff > 5:
                strengths.append({
                    'metric': self.metrics[i],
                    'score': employee_scores[i],
                    'vs_average': f"+{diff:.1f}"
                })
            elif diff < -5:
                weaknesses.append({
                    'metric': self.metrics[i],
                    'score': employee_scores[i],
                    'vs_average': f"{diff:.1f}"
                })
        
        return {'strengths': strengths, 'weaknesses': weaknesses}
    
    def calculate_team_balance(self):
        """Check if team is balanced across metrics"""
        metric_stds = np.std(self.performance_data, axis=0)
        metric_avgs = self.get_metric_averages()
        
        # Coefficient of variation (CV) = std/mean
        cv = (metric_stds / metric_avgs) * 100
        
        balance_report = []
        for i, metric in enumerate(self.metrics):
            status = "Balanced" if cv[i] < 15 else "Unbalanced"
            balance_report.append({
                'metric': metric,
                'average': metric_avgs[i],
                'std_dev': metric_stds[i],
                'cv': cv[i],
                'status': status
            })
        
        return balance_report
    
    def predict_performance_trend(self):
        """Simple trend prediction based on data distribution"""
        scores = self.get_employee_scores()
        
        # Calculate quartiles
        q1 = np.percentile(scores, 25)
        q2 = np.percentile(scores, 50)
        q3 = np.percentile(scores, 75)
        
        # Count employees in each quartile
        top = np.sum(scores >= q3)
        middle = np.sum((scores >= q2) & (scores < q3))
        bottom = np.sum(scores < q2)
        
        return {
            'q1': q1,
            'q2_median': q2,
            'q3': q3,
            'top_performers': top,
            'middle_performers': middle,
            'needs_improvement': bottom
        }
    
    def generate_report(self, filename):
        """Generate comprehensive analysis report"""
        try:
            with open(filename, 'w') as f:
                f.write("="*70 + "\n")
                f.write("EMPLOYEE PERFORMANCE ANALYSIS REPORT\n")
                f.write("="*70 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                f.write(f"Total Employees: {len(self.employees)}\n\n")
                
                # Overall stats
                f.write("-"*70 + "\n")
                f.write("OVERALL STATISTICS\n")
                f.write("-"*70 + "\n")
                stats = self.get_overall_stats()
                f.write(f"Mean Score: {stats['mean']:.2f}\n")
                f.write(f"Median Score: {stats['median']:.2f}\n")
                f.write(f"Std Deviation: {stats['std']:.2f}\n")
                f.write(f"Range: {stats['min']:.2f} - {stats['max']:.2f}\n\n")
                
                # Top performers
                f.write("-"*70 + "\n")
                f.write("TOP 3 PERFORMERS\n")
                f.write("-"*70 + "\n")
                top = self.find_top_performers(3)
                for performer in top:
                    f.write(f"{performer['rank']}. {performer['name']}: {performer['score']:.2f}\n")
                f.write("\n")
                
                # Employee rankings
                f.write("-"*70 + "\n")
                f.write("ALL EMPLOYEE RANKINGS\n")
                f.write("-"*70 + "\n")
                rankings = self.rank_employees()
                for r in rankings:
                    f.write(f"{r['rank']:2d}. {r['name']:12s} - Score: {r['score']:.2f}\n")
                f.write("\n")
                
                # Metric averages
                f.write("-"*70 + "\n")
                f.write("METRIC AVERAGES\n")
                f.write("-"*70 + "\n")
                avgs = self.get_metric_averages()
                for i, metric in enumerate(self.metrics):
                    f.write(f"{metric:25s}: {avgs[i]:.2f}\n")
                f.write("\n")
                
                # Team balance
                f.write("-"*70 + "\n")
                f.write("TEAM BALANCE ANALYSIS\n")
                f.write("-"*70 + "\n")
                balance = self.calculate_team_balance()
                for b in balance:
                    f.write(f"{b['metric']:25s}: {b['status']:12s} (CV: {b['cv']:.1f}%)\n")
                f.write("\n")
                
                f.write("="*70 + "\n")
            
            print(f"✓ Report saved to {filename}")
            return True
        except Exception as e:
            print(f"✗ Error generating report: {e}")
            return False

# Main program
def main():
    print("="*70)
    print("EMPLOYEE PERFORMANCE ANALYZER")
    print("="*70)
    
    analyzer = EmployeeAnalyzer()
    
    while True:
        print("\nMAIN MENU:")
        print("1. Load sample data")
        print("2. Load from CSV")
        print("3. Exit")
        
        choice = input("\nChoose option (1-3): ")
        
        if choice == "1":
            analyzer.load_sample_data()
            analyzer.save_to_csv("employee_data.csv")
            
        elif choice == "2":
            filename = input("Enter CSV filename: ").strip()
            if not analyzer.load_from_csv(filename):
                continue
        
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("✗ Invalid choice!")
            continue
        
        # Analysis menu
        while True:
            print("\n" + "="*70)
            print("ANALYSIS MENU")
            print("="*70)
            print("1. View overall statistics")
            print("2. View employee rankings")
            print("3. View top performers")
            print("4. Find underperformers")
            print("5. View metric averages")
            print("6. Analyze employee (strengths/weaknesses)")
            print("7. View team balance")
            print("8. View performance distribution")
            print("9. Generate full report")
            print("10. Back to main menu")
            
            analysis_choice = input("\nChoose option (1-10): ")
            
            if analysis_choice == "1":
                stats = analyzer.get_overall_stats()
                print("\n📊 OVERALL STATISTICS:")
                print("-"*40)
                print(f"Mean Score:        {stats['mean']:.2f}")
                print(f"Median Score:      {stats['median']:.2f}")
                print(f"Std Deviation:     {stats['std']:.2f}")
                print(f"Min Score:         {stats['min']:.2f}")
                print(f"Max Score:         {stats['max']:.2f}")
            
            elif analysis_choice == "2":
                rankings = analyzer.rank_employees()
                print("\n🏆 EMPLOYEE RANKINGS:")
                print("-"*40)
                for r in rankings:
                    print(f"{r['rank']:2d}. {r['name']:12s} - {r['score']:.2f}")
            
            elif analysis_choice == "3":
                top = analyzer.find_top_performers(3)
                print("\n⭐ TOP 3 PERFORMERS:")
                print("-"*40)
                for p in top:
                    print(f"{p['rank']}. {p['name']}: {p['score']:.2f}")
            
            elif analysis_choice == "4":
                threshold = float(input("Enter threshold score (default 70): ") or 70)
                under = analyzer.find_underperformers(threshold)
                print(f"\n⚠️ UNDERPERFORMERS (Below {threshold}):")
                print("-"*40)
                if under:
                    for u in under:
                        print(f"{u['name']:12s} - {u['score']:.2f} (Gap: {u['gap']:.2f})")
                else:
                    print("✓ No underperformers found!")
            
            elif analysis_choice == "5":
                avgs = analyzer.get_metric_averages()
                print("\n📈 METRIC AVERAGES:")
                print("-"*40)
                for i, metric in enumerate(analyzer.metrics):
                    print(f"{metric:25s}: {avgs[i]:.2f}")
            
            elif analysis_choice == "6":
                print("\nEmployees:")
                for i, name in enumerate(analyzer.employees):
                    print(f"{i}. {name}")
                idx = int(input("\nEnter employee number: "))
                
                if 0 <= idx < len(analyzer.employees):
                    analysis = analyzer.identify_strengths_weaknesses(idx)
                    print(f"\n📋 ANALYSIS FOR {analyzer.employees[idx].upper()}:")
                    print("-"*40)
                    
                    if analysis['strengths']:
                        print("\n💪 STRENGTHS:")
                        for s in analysis['strengths']:
                            print(f"  {s['metric']:25s}: {s['score']:.1f} ({s['vs_average']})")
                    else:
                        print("\n💪 STRENGTHS: None significant")
                    
                    if analysis['weaknesses']:
                        print("\n⚠️ AREAS FOR IMPROVEMENT:")
                        for w in analysis['weaknesses']:
                            print(f"  {w['metric']:25s}: {w['score']:.1f} ({w['vs_average']})")
                    else:
                        print("\n⚠️ AREAS FOR IMPROVEMENT: None significant")
            
            elif analysis_choice == "7":
                balance = analyzer.calculate_team_balance()
                print("\n⚖️ TEAM BALANCE ANALYSIS:")
                print("-"*40)
                for b in balance:
                    status_icon = "✓" if b['status'] == "Balanced" else "⚠️"
                    print(f"{status_icon} {b['metric']:25s}: {b['status']:12s} (CV: {b['cv']:.1f}%)")
            
            elif analysis_choice == "8":
                dist = analyzer.predict_performance_trend()
                print("\n📊 PERFORMANCE DISTRIBUTION:")
                print("-"*40)
                print(f"25th Percentile (Q1): {dist['q1']:.2f}")
                print(f"50th Percentile (Q2): {dist['q2_median']:.2f}")
                print(f"75th Percentile (Q3): {dist['q3']:.2f}")
                print(f"\nTop Performers (Q3+):      {dist['top_performers']} employees")
                print(f"Middle Performers (Q2-Q3): {dist['middle_performers']} employees")
                print(f"Needs Improvement (<Q2):   {dist['needs_improvement']} employees")
            
            elif analysis_choice == "9":
                filename = input("Enter report filename (default: 'performance_report.txt'): ").strip()
                if not filename:
                    filename = "performance_report.txt"
                analyzer.generate_report(filename)
            
            elif analysis_choice == "10":
                break
            
            else:
                print("✗ Invalid choice!")

if __name__ == "__main__":
    main()