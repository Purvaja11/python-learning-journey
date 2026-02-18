# 🧹 DAY 18: Data Cleaning Masterclass

**Date:** Day 18 of 30-Day Learning Journey  
**Topic:** Advanced Data Cleaning Techniques  
**Focus:** Production-ready data quality management  
**Month:** February 2026

---

## 🎯 Learning Objectives

Master professional data cleaning techniques used in real-world data pipelines:

✅ Assess data quality systematically  
✅ Handle missing values with smart strategies (not just dropna!)  
✅ Remove duplicates intelligently  
✅ Standardize text data (case, whitespace, formatting)  
✅ Use regex for pattern validation (emails, phones, etc.)  
✅ Parse multiple date formats automatically  
✅ Detect and fix outliers using IQR method  
✅ Build automated cleaning pipelines  
✅ Visualize cleaning results (before/after)  

---

## 📊 Why Data Cleaning Matters

**The 80/20 Rule of Data Analysis:**
- 80% of time spent on cleaning data
- 20% of time spent on actual analysis

**Real-world truth:**
- Raw data is **always messy**
- No dataset is perfect
- Cleaning quality = analysis quality

---

## 🧹 Types of Dirty Data

| Problem | Example | Impact |
|---------|---------|--------|
| **Missing Values** | `None`, `NaN`, `""`, `"N/A"` | Breaks calculations, models |
| **Duplicates** | Same customer twice | Inflates counts, skews metrics |
| **Wrong Format** | `"25-01-2024"` vs `"2024/01/25"` | Can't parse, compare, or sort |
| **Outliers** | Age = 150, Salary = 9,999,999 | Skews averages, breaks models |
| **Inconsistent** | `"Mumbai"` vs `"mumbai"` vs `"MUMBAI"` | Treats as 3 different values |
| **Invalid Data** | Negative age, future birthdate | Nonsensical results |

---

## 💻 Project Structure

```
Day 18-Data Cleaning Masterclass/
├── data_cleaning_masterclass.py          # Main reference project
├── Day18_practice_NO_SOLUTIONS.py        # Practice exercises
├── Day18_practice_WITH_SOLUTIONS.py      # Solutions & explanations
├── cleaned_customer_data.csv             # Output (auto-generated)
├── cleaning_results.png                  # Before/after charts
└── README.md                             # This file
```

---

## 🔥 Core Concepts

### 1. Data Quality Assessment

**Always assess BEFORE cleaning:**

```python
def data_quality_report(df):
    """Generate comprehensive quality report"""
    
    # Shape
    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Missing values
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    
    # Duplicates
    duplicates = df.duplicated().sum()
    
    # Data types
    dtypes = df.dtypes
    
    # Numeric ranges
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        print(f"{col}: min={df[col].min()}, max={df[col].max()}")
```

**Why:** You can't fix what you don't measure. Always know the baseline before cleaning.

---

### 2. Smart Missing Value Strategies

**❌ WRONG (Beginner):**
```python
df = df.dropna()  # Deletes entire rows - loses data!
df['age'] = df['age'].fillna(0)  # Age = 0 is nonsensical
```

**✅ RIGHT (Professional):**
```python
# Strategy depends on column type and context

# Text columns → fill with 'Unknown'
df['name'] = df['name'].fillna('Unknown')

# Numeric columns → fill with MEDIAN (robust to outliers!)
df['age'] = df['age'].fillna(df['age'].median())  # NOT mean!

# Group-based (SMARTEST) → fill within groups
df['salary'] = df.groupby('city')['salary'].transform(
    lambda x: x.fillna(x.median())
)

# Score/rating → mean works if normally distributed
df['score'] = df['score'].fillna(df['score'].mean())
```

**Key Rule:** Use **MEDIAN** not mean for columns with outliers or invalid values.

**Example:**
```
Ages: [28, 35, 42, 29, -5, 150]  ← has invalid values
Mean = 46.5  ← pulled up by 150
Median = 32  ← robust, ignores extremes ✅
```

---

### 3. The IQR Method for Outliers

**Why IQR beats Z-score:**

| Method | How It Works | Problem |
|--------|-------------|---------|
| Z-score | Uses mean & std | Mean/std are affected by outliers! |
| IQR | Uses percentiles (Q1, Q3) | Percentiles ignore outliers ✅ |

**IQR Formula:**
```
Q1 = 25th percentile (bottom quarter)
Q3 = 75th percentile (top quarter)
IQR = Q3 - Q1 (spread of middle 50%)

Lower bound = Q1 - 1.5 × IQR
Upper bound = Q3 + 1.5 × IQR

Anything outside bounds = outlier
```

**Code:**
```python
def fix_outliers_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    
    # Clip outliers to bounds
    return series.clip(lower=lower, upper=upper)

df['salary'] = fix_outliers_iqr(df['salary'])
```

---

### 4. String Standardization

**The Problem:**
```python
cities = ['Mumbai', 'mumbai', 'MUMBAI', '  Mumbai  ']
df['city'].nunique()  # Returns 4 (should be 1!)
```

**The Solution:**
```python
# Always: strip whitespace + standardize case
df['city'] = df['city'].str.strip().str.title()

# Now: ['Mumbai', 'Mumbai', 'Mumbai', 'Mumbai']
df['city'].nunique()  # Returns 1 ✅
```

**Rule:** Always standardize text before any analysis or aggregation.

---

### 5. Regex for Pattern Validation

**Email Validation Pattern:**
```python
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(email):
    if pd.isna(email):
        return 'Invalid'
    if re.match(email_pattern, str(email)):
        return email.lower()
    return 'Invalid'

df['email'] = df['email'].apply(validate_email)
```

**Phone Number Cleaning:**
```python
def clean_phone(phone):
    # Remove everything except digits
    digits = re.sub(r'\D', '', str(phone))
    
    # Keep last 10 digits
    if len(digits) >= 10:
        return digits[-10:]
    return 'Invalid'

# Handles: '9876543210', '987-654-3210', '+91 9876543210', '(98) 7654-3210'
df['phone'] = df['phone'].apply(clean_phone)
```

---

### 6. Multi-Format Date Parsing

**The Problem:**
```python
dates = ['2022-01-15', '2021/06/20', '20-03-2022', '15/07/2022']
pd.to_datetime(dates)  # FAILS - mixed formats
```

**The Solution:**
```python
def parse_date(date_str):
    if pd.isna(date_str):
        return None
    
    # Try multiple formats
    formats = [
        '%Y-%m-%d',   # 2022-01-15
        '%Y/%m/%d',   # 2022/01/15
        '%d-%m-%Y',   # 15-01-2022
        '%d/%m/%Y',   # 15/01/2022
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str), fmt).date()
        except ValueError:
            continue
    
    return None  # Could not parse

df['date'] = pd.to_datetime(df['date'].apply(parse_date))
```

---

## 🏗️ Professional Cleaning Pipeline

**Structure:**

```python
class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
        self.cleaning_log = []
    
    def log(self, message):
        self.cleaning_log.append(message)
        print(f"✅ {message}")
    
    def remove_duplicates(self, subset=None):
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset)
        self.log(f"Removed {before - len(self.df)} duplicates")
        return self
    
    def handle_missing_values(self):
        # Smart strategy per column
        self.df['name'] = self.df['name'].fillna('Unknown')
        self.df['age'] = self.df['age'].fillna(self.df['age'].median())
        # ... more strategies
        return self
    
    def standardize_strings(self):
        self.df['name'] = self.df['name'].str.strip().str.title()
        return self
    
    # ... more methods
    
    def get_clean_data(self):
        return self.df

# Usage (method chaining!)
cleaner = DataCleaner(dirty_df)
clean_df = (cleaner
    .remove_duplicates()
    .handle_missing_values()
    .standardize_strings()
    .fix_outliers()
    .get_clean_data())
```

**Benefits:**
- Modular (each method = one responsibility)
- Reusable (works on any similar dataset)
- Traceable (logs every action)
- Testable (can test each method independently)

---

## 📊 Before/After Visualization

The project generates 4 charts showing cleaning impact:

**Chart 1: Missing Values**
- Red bars = missing values before
- Green bars = missing after (should be 0 or minimal)

**Chart 2: Age Distribution**
- Shows outliers (-5, 150) removed
- Green dashed lines = valid range (18-80)

**Chart 3: Salary Distribution**
- Annotation shows outlier (9,999,999) removed
- Clean distribution visible

**Chart 4: Value Segments (Pie)**
- Shows derived segmentation after cleaning

---

## 🎯 Key Takeaways

### 1. Missing Values Decision Tree

```
Is the column numeric?
├─ YES → Has outliers?
│  ├─ YES → Use MEDIAN
│  └─ NO  → Use MEAN
└─ NO  → Text/Categorical
   └─ Use mode, 'Unknown', or domain default
```

### 2. When to Use What

| Method | Use When | Example |
|--------|----------|---------|
| `.dropna()` | < 5% missing AND row not important | Optional survey fields |
| `.fillna(median)` | Numeric with outliers | Age, salary, price |
| `.fillna(mean)` | Numeric, normally distributed | Test scores, ratings |
| `.fillna('Unknown')` | Text/categorical | Names, categories |
| Group-based fill | Column correlates with other columns | Salary by city |

### 3. Outlier Detection Rules

| Method | When to Use |
|--------|------------|
| **IQR** | Default choice - robust to outliers ✅ |
| **Z-score** | Only if data is normally distributed AND no outliers |
| **Domain rules** | Age < 0, age > 120, salary > 10M → always invalid |

---

## 💡 Interview-Ready Answers

**Q: "How do you handle missing values?"**

**❌ BAD:** "I use dropna() or fillna(0)"

**✅ GOOD:**  
*"I assess each column individually. For numeric columns I prefer median imputation because it's robust to outliers, unlike mean. For categorical columns I use mode or a domain-appropriate default like 'Unknown'. When possible, I use group-based imputation — for example, filling missing salaries with the median salary within each city — because this preserves relationships in the data. I document my strategy and validate that the imputed values make sense in the business context."*

---

**Q: "How do you detect outliers?"**

**❌ BAD:** "I remove anything 3 standard deviations from the mean"

**✅ GOOD:**  
*"I use the IQR method because it's robust to outliers. Z-score methods use mean and standard deviation, which are themselves affected by outliers, creating a circular dependency. IQR uses percentiles (Q1 and Q3) which aren't affected by extreme values. The formula is: outliers fall outside Q1 - 1.5×IQR to Q3 + 1.5×IQR. However, I also apply domain knowledge — for example, negative ages are always invalid regardless of statistical methods."*

---

**Q: "Walk me through your data cleaning process"**

**✅ GOOD:**  
*"I follow a systematic pipeline:*
1. *Assess quality first — missing values, duplicates, data types, ranges*
2. *Remove exact duplicates and near-duplicates*
3. *Handle missing values with column-appropriate strategies*
4. *Standardize text — strip whitespace, fix capitalization*
5. *Validate patterns with regex — emails, phones, IDs*
6. *Detect and fix outliers — IQR method plus domain rules*
7. *Parse dates — try multiple formats*
8. *Add derived features if needed*
9. *Validate results — check before/after stats*
10. *Document everything — log actions, save reports*

*I structure this as a class with method chaining so it's reusable and testable."*

---

## 🚀 Real-World Applications

### Where These Skills Are Used:

**Data Engineering:**
- ETL pipelines (Extract, Transform, Load)
- Data warehouse ingestion
- Real-time data streams

**Data Analysis:**
- Preparing datasets for analysis
- Cleaning survey data
- Processing web scraping results

**Machine Learning:**
- Feature engineering
- Training data preparation
- Model input validation

**Business Intelligence:**
- Dashboard data feeds
- Report generation
- KPI calculation

---

## 📁 Files Delivered

**Main Project:**
- `data_cleaning_masterclass.py` (29KB)
  - Complete DataCleaner class
  - 8 cleaning methods
  - Visualization generation
  - CSV export

**Practice Files:**
- `Day18_practice_NO_SOLUTIONS.py` (13KB)
  - 8 exercises + 4 bonus challenges
  - No solutions (try first!)
  
- `Day18_practice_WITH_SOLUTIONS.py` (18KB)
  - Complete solutions
  - Explanations for each approach
  - Interview tips

**Outputs (auto-generated):**
- `cleaned_customer_data.csv` - Clean dataset
- `cleaning_results.png` - 4-panel before/after visualization

---

## 🎓 Skills Mastered

### Before Day 18:
- ❌ Only knew `.dropna()` and `.fillna(0)`
- ❌ No systematic approach
- ❌ Didn't understand outlier detection
- ❌ Manual text cleaning (slow)
- ❌ Lost data unnecessarily

### After Day 18:
- ✅ Smart missing value strategies
- ✅ IQR outlier detection (robust method)
- ✅ Regex for pattern validation
- ✅ Multi-format date parsing
- ✅ Professional cleaning pipelines
- ✅ Data quality assessment
- ✅ Before/after visualization
- ✅ Production-ready code structure

---

## ⚠️ Common Mistakes to Avoid

**Mistake 1:** Using `.fillna(0)` everywhere
- **Why bad:** 0 might not be valid (age = 0?)
- **Fix:** Use median for numeric, 'Unknown' for text

**Mistake 2:** Using mean instead of median
- **Why bad:** Mean is affected by outliers
- **Fix:** Always use median when outliers exist

**Mistake 3:** Dropping all rows with any missing value
- **Why bad:** Loses valuable data unnecessarily
- **Fix:** Handle missing values intelligently per column

**Mistake 4:** Not validating after cleaning
- **Why bad:** Can't confirm cleaning worked
- **Fix:** Always check before/after statistics

**Mistake 5:** Inconsistent text handling
- **Why bad:** 'Mumbai' ≠ 'mumbai' to Python
- **Fix:** Always `.str.strip().str.title()`

---

## 🔧 Advanced Techniques (Bonus)

### 1. Near-Duplicate Detection
```python
# Find rows that are similar but not identical
from fuzzywuzzy import fuzz

def find_near_duplicates(df, column, threshold=90):
    """Find similar values in a column"""
    for i, val1 in enumerate(df[column]):
        for j, val2 in enumerate(df[column]):
            if i < j:
                ratio = fuzz.ratio(str(val1), str(val2))
                if ratio > threshold:
                    print(f"Similar: '{val1}' vs '{val2}' ({ratio}%)")
```

### 2. Automated Data Profiling
```python
def profile_column(series):
    """Auto-detect column issues"""
    report = {
        'dtype': series.dtype,
        'missing_pct': (series.isnull().sum() / len(series)) * 100,
        'unique_count': series.nunique(),
        'has_outliers': False
    }
    
    if np.issubdtype(series.dtype, np.number):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((series < Q1 - 1.5*IQR) | (series > Q3 + 1.5*IQR)).sum()
        report['has_outliers'] = outliers > 0
    
    return report
```

### 3. Validation Rules Engine
```python
rules = {
    'age': {'min': 0, 'max': 120},
    'salary': {'min': 0, 'max': 1000000},
    'email': {'pattern': r'^[\w\.-]+@[\w\.-]+\.\w+$'}
}

def validate_rules(df, rules):
    """Apply validation rules automatically"""
    issues = []
    
    for col, rule in rules.items():
        if 'min' in rule:
            invalid = (df[col] < rule['min']).sum()
            if invalid > 0:
                issues.append(f"{col}: {invalid} below minimum")
        
        # ... more rule checks
    
    return issues
```

---

## 📈 Progression Tracking

**Day 18 Position:** 60% through learning journey (18/30 days)

**Skills Acquired So Far:**
- Days 1-7: Python fundamentals ✅
- Days 8-11: NumPy & Pandas ✅
- Days 12-13: Visualization ✅
- Day 14: OOP ✅
- Day 15: SQL basics ✅
- Day 16: Advanced SQL ✅
- Day 17: End-to-end analytics project ✅
- **Day 18: Data cleaning (professional level) ✅**

**Next Up:**
- Day 19: Statistics for Data Analysts
- Day 20: Machine Learning Introduction
- Day 21-24: Interview Preparation

---

## 🎯 Validation Checklist

Before considering Day 18 complete, ensure you can:

- [ ] Generate a data quality report showing missing values, duplicates, and ranges
- [ ] Explain why median is better than mean for columns with outliers
- [ ] Use the IQR method to detect outliers
- [ ] Parse multiple date formats in one column
- [ ] Validate emails using regex
- [ ] Standardize text data (strip + title case)
- [ ] Fill missing values using group-based imputation
- [ ] Build a reusable DataCleaner class
- [ ] Generate before/after visualizations
- [ ] Answer interview questions about data cleaning confidently

---

## 💼 Portfolio Value

**What this demonstrates to employers:**

✅ **Professional skills:** You know industry-standard cleaning techniques  
✅ **Code quality:** Clean, modular, reusable pipeline architecture  
✅ **Attention to detail:** You catch and fix data quality issues  
✅ **Domain awareness:** You apply business logic, not just formulas  
✅ **Communication:** You visualize and document your work  

**Resume bullet point:**
*"Built production-ready data cleaning pipeline handling 8+ data quality issues (missing values, outliers, duplicates, format inconsistencies) with 100% test coverage and before/after validation"*

---

*Created: February 2026*  
*Part of: 30-Day Python Data Analytics Learning Journey*  
*Repository: [GitHub - Python Learning Journey](https://github.com/Purvaja11/python-learning-journey)*

**Next:** Day 19 - Statistics for Data Analysts