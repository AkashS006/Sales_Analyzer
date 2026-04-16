"""
datagenerator.py
─────────────────────────────────────────────────────────────────
Generates REALISTIC repeated customer purchase data for ML prediction:
  - Each customer buys 5–40 times (realistic repeat behavior)
  - Purchase datetime includes random time (09:00 – 18:00)
  - Customer preferences are STICKY (they tend to buy same categories)
  - Purchase intervals follow realistic patterns (weekly/monthly/etc.)
  - Spending patterns are consistent per customer segment

Output:
    Data/sales.csv    → ~5000+ rows  (repeated customers)
    Data/user.csv     → 300 unique customers
    Data/stocks.csv   → all products with stock
    Data/employee.csv → 20 employees
─────────────────────────────────────────────────────────────────
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ── Paths ──────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
DATA_DIR     = os.path.join(BASE_DIR, "Data")
SALES_CSV    = os.path.join(DATA_DIR, "sales.csv")
USER_CSV     = os.path.join(DATA_DIR, "user.csv")
STOCKS_CSV   = os.path.join(DATA_DIR, "stocks.csv")
EMPLOYEE_CSV = os.path.join(DATA_DIR, "employee.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# ── Constants ──────────────────────────────────────────────────
NUM_CUSTOMERS = 300
NUM_EMPLOYEES = 20

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Chennai",
    "Hyderabad", "Kolkata", "Pune", "Ahmedabad",
    "Jaipur", "Surat"
]

GENDERS  = ["Male", "Female", "Other"]
SEGMENTS = ["Regular", "Premium", "VIP", "New Customer"]
PAYMENTS = ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking", "Wallet"]
CHANNELS = ["In-Store", "Online", "Phone", "Mobile App"]

# ── Purchase frequency config per segment ─────────────────────
# (min_purchases, max_purchases, avg_days_between_purchases)
SEGMENT_BEHAVIOR = {
    "VIP":          (25, 50,  7),    # buys every ~1 week
    "Premium":      (15, 30,  14),   # buys every ~2 weeks
    "Regular":      (8,  20,  21),   # buys every ~3 weeks
    "New Customer": (2,  8,   45),   # buys occasionally
}

# ── Spending multiplier per segment ───────────────────────────
SEGMENT_SPEND_MULT = {
    "VIP":          (1.3, 2.0),
    "Premium":      (1.0, 1.5),
    "Regular":      (0.8, 1.2),
    "New Customer": (0.7, 1.1),
}

# ── Category preference weights per age group ─────────────────
# Customers tend to prefer certain categories
AGE_CATEGORY_WEIGHTS = {
    "18-25": {
        "Electronics": 25, "Clothing": 20, "Books": 10,
        "Sports": 10,      "Beauty": 10,   "Toys": 5,
        "Groceries": 5,    "Furniture": 5, "Automotive": 5, "Other": 5
    },
    "26-35": {
        "Electronics": 20, "Clothing": 15, "Groceries": 15,
        "Furniture": 10,   "Sports": 10,   "Beauty": 10,
        "Books": 5,        "Automotive": 5, "Toys": 5, "Other": 5
    },
    "36-45": {
        "Groceries": 20,   "Electronics": 15, "Furniture": 15,
        "Clothing": 10,    "Automotive": 10,  "Beauty": 10,
        "Sports": 5,       "Books": 5,        "Toys": 5, "Other": 5
    },
    "46-55": {
        "Groceries": 25,   "Furniture": 15,   "Automotive": 10,
        "Electronics": 10, "Clothing": 10,    "Beauty": 10,
        "Books": 10,       "Sports": 5,       "Toys": 2, "Other": 3
    },
    "55+": {
        "Groceries": 30,   "Books": 15,       "Beauty": 10,
        "Clothing": 10,    "Furniture": 10,   "Other": 10,
        "Electronics": 7,  "Sports": 3,       "Toys": 3, "Automotive": 2
    },
}


# ═══════════════════════════════════════════════════════════════
# NAME POOLS
# ═══════════════════════════════════════════════════════════════

MALE_FIRST_NAMES = [
    "Aarav", "Arjun", "Aditya", "Akash", "Amit",
    "Anand", "Arun", "Ashok", "Ayush", "Bharat",
    "Chirag", "Deepak", "Dev", "Dhruv", "Dinesh",
    "Ganesh", "Gaurav", "Girish", "Gopal", "Harsh",
    "Harish", "Hemant", "Hitesh", "Ishaan", "Jagdish",
    "Jai", "Jatin", "Karan", "Karthik", "Kishan",
    "Kunal", "Lalit", "Lokesh", "Mahesh", "Manish",
    "Mayank", "Mohan", "Mukesh", "Naresh", "Naveen",
    "Nikhil", "Nilesh", "Nishant", "Om", "Pankaj",
    "Parth", "Piyush", "Pranav", "Pratik", "Praveen",
    "Priyank", "Rahul", "Rajesh", "Rakesh", "Ram",
    "Ramesh", "Ravi", "Ritesh", "Rohit", "Roshan",
    "Sachin", "Sagar", "Sahil", "Sanjay", "Sanket",
    "Shivam", "Shreyas", "Siddhant", "Sourav", "Sudhir",
    "Sunil", "Suresh", "Sushil", "Tarun", "Uday",
    "Vaibhav", "Vijay", "Vikas", "Vinay", "Vishal",
    "Vivek", "Yash", "Yogesh", "Zubair", "Kabir",
    "Pradeep", "Rajan", "Shyam", "Tushar", "Umesh",
    "Vikram", "Wasim", "Yusuf", "Zubin", "Balaji",
    "Bhuvan", "Dhaval", "Faisal", "Hardik", "Ishan",
]

FEMALE_FIRST_NAMES = [
    "Aarti", "Aisha", "Akanksha", "Amrita", "Ananya",
    "Anika", "Anjali", "Anushka", "Archana", "Avni",
    "Bhavna", "Deepa", "Deepika", "Divya", "Diya",
    "Durga", "Ekta", "Geeta", "Harini", "Heena",
    "Isha", "Ishita", "Jaya", "Jyoti", "Kajal",
    "Kavita", "Kavya", "Kiran", "Komal", "Kratika",
    "Lakshmi", "Lata", "Lavanya", "Madhuri", "Manasi",
    "Manisha", "Meena", "Meera", "Megha", "Mitali",
    "Monika", "Nandini", "Neha", "Nikita", "Nisha",
    "Pari", "Payal", "Pooja", "Prachi", "Pragya",
    "Priya", "Priyanka", "Radha", "Radhika", "Rakhi",
    "Ranjana", "Rashmi", "Raveena", "Rekha", "Ritu",
    "Riya", "Rohini", "Ruchi", "Rupali", "Sadhna",
    "Sakshi", "Sangita", "Sanika", "Sarita", "Seema",
    "Shreya", "Shweta", "Simran", "Sneha", "Sonal",
    "Sonia", "Sonam", "Subha", "Suchitra", "Supriya",
    "Swati", "Tanvi", "Tara", "Trisha", "Uma",
    "Urmila", "Usha", "Vandana", "Varsha", "Vaishali",
    "Vidya", "Vinita", "Vrinda", "Yamini", "Zara",
    "Zoya", "Bhavya", "Charvi", "Falak", "Gargi",
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar",
    "Patel", "Shah", "Mehta", "Joshi", "Nair",
    "Pillai", "Reddy", "Rao", "Iyer", "Menon",
    "Krishnan", "Pandey", "Mishra", "Tiwari", "Srivastava",
    "Chaudhary", "Yadav", "Dubey", "Shukla", "Tripathi",
    "Bose", "Das", "Dey", "Ghosh", "Chatterjee",
    "Banerjee", "Mukherjee", "Chakraborty", "Sen", "Roy",
    "Malhotra", "Kapoor", "Khanna", "Sethi", "Bhatia",
    "Arora", "Chadha", "Walia", "Anand", "Bajaj",
    "Agarwal", "Goyal", "Mittal", "Bansal", "Garg",
    "Jain", "Khandelwal", "Oswal", "Saraogi", "Singhania",
    "Thomas", "George", "Philip", "Mathew", "Joseph",
    "Abraham", "Cherian", "Varghese", "Antony", "Paul",
    "Hussain", "Khan", "Ansari", "Shaikh", "Siddiqui",
    "Qureshi", "Ali", "Sheikh", "Mirza", "Baig",
    "Naidu", "Murthy", "Rajan", "Subramaniam", "Venkat",
    "Balaji", "Sundar", "Ramesh", "Dinesh", "Ganesh",
    "Pawar", "Patil", "Jadhav", "Shinde", "Bhosale",
    "Desai", "Modi", "Trivedi", "Bhatt", "Doshi",
    "Naik", "Gowda", "Shetty", "Kamath", "Hegde",
]


# ── Product Catalogue ──────────────────────────────────────────
CATALOGUE = {
    "Electronics": [
        ("PS5",                    50000),
        ("iPhone 15",              79999),
        ("Samsung Galaxy S24",     69999),
        ("MacBook Air M2",         99999),
        ("Dell Laptop",            55000),
        ("Sony Headphones",         8999),
        ("Apple Watch",            41999),
        ("Smart TV 55 inch",       45000),
        ("Canon DSLR Camera",      35000),
        ("JBL Bluetooth Speaker",   4999),
        ("OnePlus Nord 4",         27999),
        ("iPad Air",               59999),
        ("Gaming Mouse",            2499),
        ("Mechanical Keyboard",     3999),
        ("USB-C Hub",               1999),
    ],
    "Clothing": [
        ("Men's Formal Shirt",      1299),
        ("Women's Kurti",            899),
        ("Denim Jeans",             1999),
        ("Sports T-Shirt",           699),
        ("Winter Jacket",           3499),
        ("Saree",                   2499),
        ("Kids Dress",               799),
        ("Leggings",                 499),
        ("Formal Trousers",         1599),
        ("Hoodie",                  1899),
    ],
    "Groceries": [
        ("Basmati Rice 5kg",         499),
        ("Toor Dal 1kg",             149),
        ("Sunflower Oil 1L",         189),
        ("Amul Butter 500g",         275),
        ("Sugar 1kg",                 55),
        ("Aashirvaad Atta 10kg",     450),
        ("Nescafe Coffee 200g",      399),
        ("Bournvita 1kg",            420),
        ("Himalaya Honey 500g",      299),
        ("Mixed Dry Fruits 500g",    699),
    ],
    "Furniture": [
        ("Office Chair",            8999),
        ("Study Table",             6499),
        ("Bookshelf",               4999),
        ("Sofa Set 3+1+1",         35000),
        ("Queen Bed Frame",        18000),
        ("Dining Table 6 Seat",    22000),
        ("Wardrobe 3 Door",        15000),
        ("Coffee Table",            4500),
        ("TV Unit",                 7500),
        ("Bean Bag",                2999),
    ],
    "Sports": [
        ("Cricket Bat",             2499),
        ("Football",                 799),
        ("Badminton Racket Set",    1299),
        ("Yoga Mat",                 999),
        ("Dumbbells Set 10kg",      2199),
        ("Cycling Helmet",          1499),
        ("Skipping Rope",            299),
        ("Tennis Racket",           3499),
        ("Swimming Goggles",         699),
        ("Treadmill",              35000),
    ],
    "Books": [
        ("Atomic Habits",            399),
        ("Rich Dad Poor Dad",        299),
        ("The Alchemist",            249),
        ("Python Crash Course",      599),
        ("Clean Code",               699),
        ("Wings of Fire",            299),
        ("Data Structures Guide",    549),
        ("Business Sutra",           449),
        ("Zero to One",              399),
        ("Deep Work",                349),
    ],
    "Toys": [
        ("LEGO Classic Set",        2999),
        ("Remote Control Car",      1499),
        ("Barbie Doll House",       3999),
        ("Rubik's Cube",             399),
        ("Board Game Monopoly",      999),
        ("Hot Wheels Track Set",    1299),
        ("Play-Doh Kit",             599),
        ("Puzzle 1000 Pieces",       799),
        ("Action Figure Set",        899),
        ("Baby Walker",             2499),
    ],
    "Beauty": [
        ("Lakme Foundation",         599),
        ("Maybelline Lipstick",      399),
        ("Nivea Body Lotion",        299),
        ("Himalaya Face Wash",       149),
        ("L'Oreal Shampoo",          399),
        ("Nykaa Kajal",              149),
        ("Biotique Face Cream",      249),
        ("Dove Soap Pack 4",         199),
        ("Set Wet Hair Gel",         149),
        ("WOW Vitamin C Serum",      599),
    ],
    "Automotive": [
        ("Car Dashboard Camera",    3999),
        ("Tyre Inflator",           2499),
        ("Car Seat Cover Set",      1999),
        ("Helmet Full Face",        2999),
        ("Jump Starter Pack",       4999),
        ("Car Vacuum Cleaner",      1499),
        ("GPS Tracker",             2999),
        ("Car Polish Kit",           899),
        ("Bike Chain Lubricant",     299),
        ("LED Car Headlight Set",   1799),
    ],
    "Other": [
        ("Stainless Steel Bottle",   599),
        ("Wall Clock",               799),
        ("Scented Candle Set",       499),
        ("Umbrella",                 399),
        ("Travel Bag",              1999),
        ("Photo Frame Set",          699),
        ("Desk Organizer",           499),
        ("Digital Weighing Scale",   999),
        ("Air Freshener",            299),
        ("Multicolour Pen Set",      199),
    ],
}

CATEGORIES = list(CATALOGUE.keys())


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def random_full_name(gender=None):
    if gender is None or gender == "Other":
        gender = random.choice(["Male", "Female"])
    first = random.choice(MALE_FIRST_NAMES if gender == "Male"
                          else FEMALE_FIRST_NAMES)
    last  = random.choice(LAST_NAMES)
    return f"{first} {last}", gender


def random_mobile():
    first = random.choice(["7", "8", "9"])
    rest  = "".join([str(random.randint(0, 9)) for _ in range(9)])
    return first + rest


def random_datetime(start: datetime, end: datetime) -> str:
    """
    Random datetime between start and end,
    with time restricted to 09:00 – 18:00 (business hours).
    """
    delta_days = (end - start).days
    rand_day   = random.randint(0, delta_days)
    dt         = start + timedelta(days=rand_day)

    # Random time: 09:00 to 18:00
    hour   = random.randint(9, 17)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    dt = dt.replace(hour=hour, minute=minute, second=second)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_age_group(age: int) -> str:
    if age < 18:   return "18-25"
    if age < 26:   return "18-25"
    if age < 36:   return "26-35"
    if age < 46:   return "36-45"
    if age < 56:   return "46-55"
    return "55+"


def pick_product_for_customer(preferred_categories: list,
                               spend_mult_range: tuple):
    """
    Pick a product biased toward the customer's preferred categories.
    75% chance from preferred category, 25% random.
    """
    if random.random() < 0.75 and preferred_categories:
        cat = random.choice(preferred_categories)
    else:
        cat = random.choice(CATEGORIES)

    name, base_price = random.choice(CATALOGUE[cat])
    mult       = random.uniform(*spend_mult_range)
    unit_price = round(base_price * mult * random.uniform(0.95, 1.05), 2)
    return cat, name, unit_price


def generate_purchase_dates(segment: str,
                             start: datetime,
                             end: datetime) -> list:
    """
    Generate realistic purchase dates for a customer
    based on their segment behavior.
    Returns a sorted list of datetime strings.
    """
    min_p, max_p, avg_gap = SEGMENT_BEHAVIOR[segment]
    num_purchases = random.randint(min_p, max_p)

    dates   = []
    current = start + timedelta(days=random.randint(0, 30))

    for _ in range(num_purchases):
        if current > end:
            break

        # Random time 09:00–18:00
        hour   = random.randint(9, 17)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        dt     = current.replace(hour=hour, minute=minute, second=second)
        dates.append(dt.strftime("%Y-%m-%d %H:%M:%S"))

        # Next purchase gap — normally distributed around avg_gap
        gap = max(1, int(np.random.normal(avg_gap, avg_gap * 0.3)))
        current += timedelta(days=gap)

    return dates


# ═══════════════════════════════════════════════════════════════
# STEP 1 — Generate Customers
# ═══════════════════════════════════════════════════════════════

print(f"Generating {NUM_CUSTOMERS} unique customers...")

START_DATE = datetime(2023, 1, 1)
END_DATE   = datetime(2026, 6, 30)

customers  = []
used_names = set()

for i in range(1, NUM_CUSTOMERS + 1):
    cid    = f"CID{i:03d}"
    gender = random.choice(GENDERS)

    while True:
        full_name, resolved_gender = random_full_name(gender)
        if full_name not in used_names:
            used_names.add(full_name)
            break

    age       = random.randint(18, 65)
    age_group = get_age_group(age)
    segment   = random.choice(SEGMENTS)

    # ── Build sticky category preferences ─────────────────────
    age_weights    = AGE_CATEGORY_WEIGHTS[age_group]
    cat_names      = list(age_weights.keys())
    cat_weights    = list(age_weights.values())
    num_preferred  = random.randint(2, 4)
    preferred_cats = random.choices(cat_names,
                                    weights=cat_weights,
                                    k=num_preferred)
    preferred_cats = list(set(preferred_cats))  # deduplicate

    # ── Preferred payment method (sticky) ─────────────────────
    preferred_payment = random.choices(
        PAYMENTS,
        weights=[10, 25, 20, 30, 8, 7],  # UPI most popular
        k=1
    )[0]

    # ── Preferred channel (sticky) ────────────────────────────
    preferred_channel = random.choices(
        CHANNELS,
        weights=[20, 40, 10, 30],  # Online & Mobile App popular
        k=1
    )[0]

    customers.append({
        "customer_id":        cid,
        "customer_name":      full_name,
        "age":                age,
        "age_group":          age_group,
        "gender":             gender,
        "mobile_number":      random_mobile(),
        "city":               random.choice(CITIES),
        "customer_segment":   segment,
        "preferred_cats":     preferred_cats,
        "preferred_payment":  preferred_payment,
        "preferred_channel":  preferred_channel,
        "spend_mult_range":   SEGMENT_SPEND_MULT[segment],
    })

cust_df = pd.DataFrame(customers)
print(f"  Customers created: {len(cust_df)}")
print(f"  Sample: {', '.join(cust_df['customer_name'].head(5).tolist())}")


# ═══════════════════════════════════════════════════════════════
# STEP 2 — Generate Sales with Realistic Repeating Patterns
# ═══════════════════════════════════════════════════════════════

print(f"\nGenerating sales rows (realistic repeating customer patterns)...")

sales_rows = []

for idx, cust in cust_df.iterrows():

    # ── Generate purchase dates for this customer ──────────────
    purchase_dates = generate_purchase_dates(
        cust["customer_segment"], START_DATE, END_DATE
    )

    if len(purchase_dates) == 0:
        continue

    preferred_cats   = cust["preferred_cats"]
    spend_mult_range = cust["spend_mult_range"]

    # ── Sometimes customer buys MULTIPLE items per visit ───────
    for pdate in purchase_dates:

        # 30% chance of buying 2 items in one visit
        items_this_visit = random.choices([1, 2, 3],
                                          weights=[65, 25, 10])[0]

        for _ in range(items_this_visit):
            cat, pname, unit_price = pick_product_for_customer(
                preferred_cats, spend_mult_range
            )

            qty = random.choices(
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                weights=[45, 25, 12, 6, 4, 3, 2, 1, 1, 1]
            )[0]

            total_spend = round(qty * unit_price, 2)

            # 80% use preferred payment, 20% random
            payment = (cust["preferred_payment"]
                       if random.random() < 0.80
                       else random.choice(PAYMENTS))

            # 80% use preferred channel, 20% random
            channel = (cust["preferred_channel"]
                       if random.random() < 0.80
                       else random.choice(CHANNELS))

            sales_rows.append({
                "customer_id":       cust["customer_id"],
                "customer_name":     cust["customer_name"],
                "age":               cust["age"],
                "gender":            cust["gender"],
                "mobile_number":     cust["mobile_number"],
                "city":              cust["city"],
                "purchase_date":     pdate,
                "product_category":  cat,
                "product_name":      pname,
                "quantity":          qty,
                "unit_price":        unit_price,
                "total_spend":       total_spend,
                "payment_method":    payment,
                "channel":           channel,
                "customer_segment":  cust["customer_segment"],
            })

    if (idx + 1) % 50 == 0:
        print(f"  ... {idx + 1}/{NUM_CUSTOMERS} customers processed "
              f"| {len(sales_rows):,} rows so far")

sales_df = (pd.DataFrame(sales_rows)
            .sort_values("purchase_date")
            .reset_index(drop=True))

print(f"\n  Total sales rows generated : {len(sales_df):,}")
print(f"  Unique customers in sales  : {sales_df['customer_id'].nunique()}")
print(f"  Avg purchases per customer : "
      f"{len(sales_df) / sales_df['customer_id'].nunique():.1f}")
print(f"  Date range : {sales_df['purchase_date'].min()} "
      f"→ {sales_df['purchase_date'].max()}")


# ── Quick sanity check: purchases per customer ─────────────────
purchases_per_cust = (sales_df.groupby("customer_id")
                      .size()
                      .describe())
print(f"\n  Purchases per customer stats:\n{purchases_per_cust.to_string()}")


# ═══════════════════════════════════════════════════════════════
# STEP 3 — user.csv
# ═══════════════════════════════════════════════════════════════

print("\nBuilding user.csv...")

user_df = (
    sales_df[["customer_id", "customer_name", "gender", "mobile_number"]]
    .drop_duplicates(subset=["customer_id"])
    .sort_values("customer_id")
    .reset_index(drop=True)
)
print(f"  Unique customers : {len(user_df)}")


# ═══════════════════════════════════════════════════════════════
# STEP 4 — stocks.csv
# ═══════════════════════════════════════════════════════════════

print("\nBuilding stocks.csv...")

stock_rows = []
pid = 1
for cat, products in CATALOGUE.items():
    for pname, base_price in products:
        stock_rows.append({
            "product_id":   f"PRD{pid:03d}",
            "product_name": pname,
            "category":     cat,
            "quantity":     random.randint(10, 500),
            "unit_price":   round(base_price * random.uniform(0.97, 1.03), 2),
            "added_date":   random_datetime(
                datetime(2023, 1, 1), datetime(2024, 12, 31)
            )[:10],
        })
        pid += 1

stocks_df = pd.DataFrame(stock_rows)
print(f"  Unique products : {len(stocks_df)}")


# ═══════════════════════════════════════════════════════════════
# STEP 5 — employee.csv
# ═══════════════════════════════════════════════════════════════

print("\nBuilding employee.csv...")

ROLES = [
    "Sales Executive", "Store Manager", "Cashier",
    "Inventory Manager", "Sales Associate", "Team Lead",
    "Customer Support", "Billing Executive", "Floor Manager",
    "HR Manager",
]

emp_rows       = []
used_emp_names = set()

for i in range(1, NUM_EMPLOYEES + 1):
    gender = random.choice(["Male", "Female"])
    while True:
        full_name, _ = random_full_name(gender)
        if full_name not in used_emp_names and full_name not in used_names:
            used_emp_names.add(full_name)
            break

    emp_rows.append({
        "employee_id":   f"EMP{i:03d}",
        "employee_name": full_name,
        "gender":        gender,
        "mobile_number": random_mobile(),
        "role":          random.choice(ROLES),
        "city":          random.choice(CITIES),
        "join_date":     random_datetime(
            datetime(2019, 1, 1), datetime(2024, 12, 31)
        )[:10],
    })

emp_df = pd.DataFrame(emp_rows)
print(f"  Employees : {len(emp_df)}")


# ═══════════════════════════════════════════════════════════════
# STEP 6 — Save All CSVs
# ═══════════════════════════════════════════════════════════════

print("\nSaving CSV files...")

sales_df.to_csv(SALES_CSV,    index=False, encoding="utf-8")
user_df.to_csv(USER_CSV,      index=False, encoding="utf-8")
stocks_df.to_csv(STOCKS_CSV,  index=False, encoding="utf-8")
emp_df.to_csv(EMPLOYEE_CSV,   index=False, encoding="utf-8")

print(f"  sales.csv    saved : {len(sales_df):,} rows")
print(f"  user.csv     saved : {len(user_df):,} rows")
print(f"  stocks.csv   saved : {len(stocks_df):,} rows")
print(f"  employee.csv saved : {len(emp_df):,} rows")


# ═══════════════════════════════════════════════════════════════
# STEP 7 — Summary Report
# ═══════════════════════════════════════════════════════════════

total_rev        = sales_df["total_spend"].sum()
avg_spend_cust   = sales_df.groupby("customer_id")["total_spend"].mean().mean()
top_cat          = sales_df.groupby("product_category")["total_spend"].sum().idxmax()
top_city         = sales_df["city"].value_counts().idxmax()
top_payment      = sales_df["payment_method"].value_counts().idxmax()
top_channel      = sales_df["channel"].value_counts().idxmax()
avg_purchases    = len(sales_df) / sales_df["customer_id"].nunique()

# Segment breakdown
seg_counts = sales_df.groupby("customer_segment")["customer_id"].nunique()

print("\n" + "=" * 65)
print("   DATA GENERATION COMPLETE — REALISTIC REPEAT PURCHASE DATA")
print("=" * 65)
print(f"  Total Sales Rows       : {len(sales_df):,}")
print(f"  Total Revenue          : Rs {total_rev:,.2f}")
print(f"  Unique Customers       : {sales_df['customer_id'].nunique():,}")
print(f"  Avg Purchases/Customer : {avg_purchases:.1f}")
print(f"  Avg Spend/Customer     : Rs {avg_spend_cust:,.2f}")
print(f"  Unique Products        : {len(stocks_df):,}")
print(f"  Employees              : {len(emp_df):,}")
print(f"  Date Range             : 2023-01-01 09:00:00 -> 2026-06-30 18:00:00")
print(f"  Top Category           : {top_cat}")
print(f"  Top City               : {top_city}")
print(f"  Top Payment Method     : {top_payment}")
print(f"  Top Channel            : {top_channel}")
print(f"\n  Segment Breakdown (unique customers):")
for seg, cnt in seg_counts.items():
    print(f"    {seg:<16} : {cnt:,} customers")
print("=" * 65)
print("\n  Now run:  python app.py")
print("=" * 65)
