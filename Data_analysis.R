# ════════════════════════════════════════════════════════════════
#  Data_analysis.R
#  Project: Sales Data Analysis & Prediction Pipeline
#  Flow: Step by step validation → Clean → EDA → Predict
# ════════════════════════════════════════════════════════════════


# ────────────────────────────────────────────────────────────────
# STEP 0 — Install & Load Packages
# ────────────────────────────────────────────────────────────────

required_packages <- c(
  "tidyverse", "lubridate", "ggplot2",
  "dplyr",     "scales",    "corrplot",
  "ggcorrplot","skimr",     "janitor",
  "gridExtra", "RColorBrewer", "viridis",
  "knitr",     "reshape2",  "ggridges",
  "moments"
)

missing_pkg <- required_packages[
  !required_packages %in% rownames(installed.packages())
]

if (length(missing_pkg) > 0) {
  cat("Installing missing packages:", 
      paste(missing_pkg, collapse = ", "), "\n")
  install.packages(missing_pkg)
} else {
  cat("All packages already installed.\n")
}

library(tidyverse)
library(lubridate)
library(ggplot2)
library(dplyr)
library(scales)
library(corrplot)
library(ggcorrplot)
library(skimr)
library(janitor)
library(gridExtra)
library(RColorBrewer)
library(viridis)
library(reshape2)
library(ggridges)
library(moments)

cat("All packages loaded successfully!\n")

# ────────────────────────────────────────────────────────────────
# STEP 1 — Define Paths & Load Data
# ────────────────────────────────────────────────────────────────

# ── Detect Project root ────────────────────────────────────────
project_root  <- dirname(rstudioapi::getSourceEditorContext()$path)

# ── Build all paths ────────────────────────────────────────────
source_file   <- file.path(project_root, "Data", "sales.csv")
processed_dir <- file.path(project_root, "Processed Data")
dest_file     <- file.path(processed_dir, "process_sales_data.csv")

# ── Print paths to verify ──────────────────────────────────────
cat("══════════════════════════════════════\n")
cat("  PATH CONFIGURATION\n")
cat("══════════════════════════════════════\n")
cat("Project root  :", project_root,  "\n")
cat("Source file   :", source_file,   "\n")
cat("Processed dir :", processed_dir, "\n")
cat("Dest file     :", dest_file,     "\n")
cat("══════════════════════════════════════\n")

# ── Check source file exists ───────────────────────────────────
if (!file.exists(source_file)) {
  stop("ERROR: sales.csv not found! Check path: ", source_file)
} else {
  cat("sales.csv found!\n")
}

# ── Create Processed Data folder if needed ─────────────────────
if (!dir.exists(processed_dir)) {
  dir.create(processed_dir, recursive = TRUE)
  cat("Processed Data folder created.\n")
} else {
  cat("Processed Data folder already exists.\n")
}

# ── Copy file ──────────────────────────────────────────────────
copied <- file.copy(
  from      = source_file,
  to        = dest_file,
  overwrite = TRUE
)

if (copied) {
  cat("sales.csv copied to Processed Data folder.\n")
} else {
  cat("ERROR: File copy failed!\n")
}

# ── Load the copied file ───────────────────────────────────────
df_raw <- read.csv(
  dest_file,
  stringsAsFactors = FALSE,
  na.strings       = c("", "NA", "N/A",
                       "null", "NULL",
                       "None", " ")
)

cat("\n══════════════════════════════════════\n")
cat("  DATASET LOADED SUCCESSFULLY\n")
cat("══════════════════════════════════════\n")
cat("Rows      :", nrow(df_raw), "\n")
cat("Columns   :", ncol(df_raw), "\n")
cat("File size :", 
    round(file.size(dest_file) / 1024, 2), "KB\n")
cat("══════════════════════════════════════\n")




# ────────────────────────────────────────────────────────────────
# STEP 2 — First Look at Data
# ────────────────────────────────────────────────────────────────

cat("══════════════════════════════════════\n")
cat("  2A — COLUMN NAMES & TYPES\n")
cat("══════════════════════════════════════\n")

# ── Column names ───────────────────────────────────────────────
cat("Column Names:\n")
print(colnames(df_raw))

# ── Data types ─────────────────────────────────────────────────
cat("\nData Types:\n")
print(sapply(df_raw, class))

cat("\n══════════════════════════════════════\n")
cat("  2B — FIRST 5 ROWS\n")
cat("══════════════════════════════════════\n")
print(head(df_raw, 5))

cat("\n══════════════════════════════════════\n")
cat("  2C — LAST 5 ROWS\n")
cat("══════════════════════════════════════\n")
print(tail(df_raw, 5))

cat("\n══════════════════════════════════════\n")
cat("  2D — STRUCTURE OVERVIEW\n")
cat("══════════════════════════════════════\n")
glimpse(df_raw)

cat("\n══════════════════════════════════════\n")
cat("  2E — UNIQUE VALUES PER COLUMN\n")
cat("══════════════════════════════════════\n")
unique_counts <- data.frame(
  Column        = colnames(df_raw),
  Type          = sapply(df_raw, class),
  Unique_Values = sapply(df_raw, n_distinct),
  Missing       = sapply(df_raw, function(x) sum(is.na(x))),
  row.names     = NULL
)
print(unique_counts)

cat("\n══════════════════════════════════════\n")
cat("  2F — CATEGORY VALUE INSPECTION\n")
cat("══════════════════════════════════════\n")
cat("Gender values     :", 
    paste(unique(df_raw$gender), 
          collapse = " | "), "\n")
cat("Segment values    :", 
    paste(unique(df_raw$customer_segment), 
          collapse = " | "), "\n")
cat("Payment values    :", 
    paste(unique(df_raw$payment_method), 
          collapse = " | "), "\n")
cat("Channel values    :", 
    paste(unique(df_raw$channel), 
          collapse = " | "), "\n")
cat("Category values   :", 
    paste(unique(df_raw$product_category), 
          collapse = " | "), "\n")
cat("City values       :", 
    paste(unique(df_raw$city), 
          collapse = " | "), "\n")

cat("\n══════════════════════════════════════\n")
cat("  2G — DATE RANGE CHECK\n")
cat("══════════════════════════════════════\n")
cat("Date column sample:\n")
print(head(df_raw$purchase_date, 5))
cat("\nEarliest date :", 
    min(df_raw$purchase_date, na.rm = TRUE), "\n")
cat("Latest date   :", 
    max(df_raw$purchase_date, na.rm = TRUE), "\n")

cat("\n══════════════════════════════════════\n")
cat("  2H — KEY BUSINESS NUMBERS\n")
cat("══════════════════════════════════════\n")
cat("Unique customers   :", 
    n_distinct(df_raw$customer_id),   "\n")
cat("Unique products    :", 
    n_distinct(df_raw$product_name),  "\n")
cat("Unique categories  :", 
    n_distinct(df_raw$product_category), "\n")
cat("Avg purchases/cust :", 
    round(nrow(df_raw) / 
            n_distinct(df_raw$customer_id), 1), "\n")
cat("Total revenue (Rs) :", 
    format(round(sum(df_raw$total_spend, 
                     na.rm = TRUE), 0),
           big.mark = ","), "\n")
cat("Avg spend/txn (Rs) :", 
    format(round(mean(df_raw$total_spend, 
                      na.rm = TRUE), 2),
           big.mark = ","), "\n")



# ────────────────────────────────────────────────────────────────
# STEP 3 — Statistical Summary
# ────────────────────────────────────────────────────────────────

cat("══════════════════════════════════════\n")
cat("  3A — NUMERIC COLUMNS SUMMARY\n")
cat("══════════════════════════════════════\n")

# ── Summary of numeric columns ─────────────────────────────────
num_summary <- df_raw %>%
  select(age, quantity, unit_price, total_spend) %>%
  summary()
print(num_summary)

cat("\n══════════════════════════════════════\n")
cat("  3B — DETAILED NUMERIC STATS\n")
cat("══════════════════════════════════════\n")

# ── Custom detailed stats per numeric column ───────────────────
num_cols <- c("age", "quantity", "unit_price", "total_spend")

for (col in num_cols) {
  vals <- df_raw[[col]]
  cat("\n──────────────────────────────────\n")
  cat("Column      :", col, "\n")
  cat("Min         :", round(min(vals,      na.rm = TRUE), 2), "\n")
  cat("Max         :", round(max(vals,      na.rm = TRUE), 2), "\n")
  cat("Mean        :", round(mean(vals,     na.rm = TRUE), 2), "\n")
  cat("Median      :", round(median(vals,   na.rm = TRUE), 2), "\n")
  cat("Std Dev     :", round(sd(vals,       na.rm = TRUE), 2), "\n")
  cat("Variance    :", round(var(vals,      na.rm = TRUE), 2), "\n")
  cat("Skewness    :", round(skewness(vals, na.rm = TRUE), 2), "\n")
  cat("Kurtosis    :", round(kurtosis(vals, na.rm = TRUE), 2), "\n")
  cat("Q1 (25%)    :", round(quantile(vals, 0.25, na.rm = TRUE), 2), "\n")
  cat("Q3 (75%)    :", round(quantile(vals, 0.75, na.rm = TRUE), 2), "\n")
  cat("IQR         :", round(IQR(vals,      na.rm = TRUE), 2), "\n")
}

cat("\n══════════════════════════════════════\n")
cat("  3C — CATEGORICAL COLUMNS SUMMARY\n")
cat("══════════════════════════════════════\n")

cat_cols <- c("gender", "city", "customer_segment",
              "product_category", "payment_method", "channel")

for (col in cat_cols) {
  cat("\n──────────────────────────────────\n")
  cat("Column:", col, "\n")
  tbl <- sort(table(df_raw[[col]],
                    useNA = "ifany"),
              decreasing = TRUE)
  pct <- round(prop.table(tbl) * 100, 1)
  result <- data.frame(
    Value   = names(tbl),
    Count   = as.integer(tbl),
    Percent = paste0(as.numeric(pct), "%"),
    row.names = NULL
  )
  print(result)
}

cat("\n══════════════════════════════════════\n")
cat("  3D — FULL SKIM REPORT\n")
cat("══════════════════════════════════════\n")
skim(df_raw)

cat("\n══════════════════════════════════════\n")
cat("  3E — SKEWNESS INTERPRETATION\n")
cat("══════════════════════════════════════\n")

for (col in num_cols) {
  vals <- df_raw[[col]]
  skew <- round(skewness(vals, na.rm = TRUE), 2)
  interpretation <- case_when(
    abs(skew) < 0.5  ~ "Symmetric (normal)",
    abs(skew) < 1.0  ~ "Moderately skewed",
    TRUE             ~ "Highly skewed - consider log transform"
  )
  cat(sprintf("%-15s skewness = %6.2f → %s\n",
              col, skew, interpretation))
}




# ────────────────────────────────────────────────────────────────
# STEP 4 — Missing Values & Duplicate Check
# ────────────────────────────────────────────────────────────────

cat("══════════════════════════════════════\n")
cat("  4A — MISSING VALUE ANALYSIS\n")
cat("══════════════════════════════════════\n")

# ── Count missing per column ───────────────────────────────────
missing_df <- data.frame(
  Column      = colnames(df_raw),
  Missing     = sapply(df_raw, function(x) sum(is.na(x))),
  Missing_Pct = sapply(df_raw, function(x)
    round(sum(is.na(x)) / nrow(df_raw) * 100, 2)),
  Status      = sapply(df_raw, function(x) {
    pct <- sum(is.na(x)) / nrow(df_raw) * 100
    if      (pct == 0)  "CLEAN"
    else if (pct < 5)   "LOW - safe to fill"
    else if (pct < 20)  "MODERATE - fill carefully"
    else                "HIGH - consider dropping"
  }),
  row.names   = NULL
)

print(missing_df)

cat("\nTotal missing values in dataset:",
    sum(is.na(df_raw)), "\n")

cat("\nColumns with missing values:\n")
has_missing <- missing_df[missing_df$Missing > 0, ]
if (nrow(has_missing) == 0) {
  cat("None! Dataset has NO missing values.\n")
} else {
  print(has_missing)
}

cat("\n══════════════════════════════════════\n")
cat("  4B — MISSING VALUE VISUAL\n")
cat("══════════════════════════════════════\n")

# ── Visual bar chart of missing values ────────────────────────
missing_plot <- missing_df %>%
  filter(Missing > 0)

if (nrow(missing_plot) > 0) {
  ggplot(missing_plot,
         aes(x    = reorder(Column, Missing_Pct),
             y    = Missing_Pct,
             fill = Status)) +
    geom_col() +
    geom_text(aes(label = paste0(Missing_Pct, "%")),
              hjust = -0.1) +
    coord_flip() +
    labs(title = "Missing Values by Column (%)",
         x = "Column", y = "Missing %") +
    theme_minimal()
} else {
  cat("No missing values to plot.\n")
}

cat("\n══════════════════════════════════════\n")
cat("  4C — DUPLICATE ROW CHECK\n")
cat("══════════════════════════════════════\n")

# ── Full duplicates ────────────────────────────────────────────
full_dupes <- sum(duplicated(df_raw))
cat("Full duplicate rows (exact match) :", full_dupes, "\n")

if (full_dupes > 0) {
  cat("\nSample duplicate rows:\n")
  print(df_raw[duplicated(df_raw), ] %>% head(3))
}

# ── Partial duplicates ─────────────────────────────────────────
cat("\n── Partial Duplicates Check ──\n")
cat("(Same customer + same date + same product)\n\n")

partial_dupes <- df_raw %>%
  group_by(customer_id, purchase_date, product_name) %>%
  filter(n() > 1) %>%
  arrange(customer_id, purchase_date, product_name) %>%
  ungroup()

cat("Partial duplicate rows found:", nrow(partial_dupes), "\n")

if (nrow(partial_dupes) > 0) {
  cat("\nSample partial duplicates:\n")
  print(head(partial_dupes %>%
               select(customer_id, purchase_date,
                      product_name, quantity,
                      total_spend), 6))
}

cat("\n── Customer ID Consistency Check ──\n")
# Check if same customer_id always has same name
id_name_check <- df_raw %>%
  group_by(customer_id) %>%
  summarise(
    unique_names = n_distinct(customer_name),
    .groups      = "drop"
  ) %>%
  filter(unique_names > 1)

if (nrow(id_name_check) == 0) {
  cat("PASS: Every customer_id has exactly one name.\n")
} else {
  cat("FAIL: These customer_ids have multiple names:\n")
  print(id_name_check)
}

# Check if same customer_id always has same city
id_city_check <- df_raw %>%
  group_by(customer_id) %>%
  summarise(
    unique_cities = n_distinct(city),
    .groups       = "drop"
  ) %>%
  filter(unique_cities > 1)

if (nrow(id_city_check) == 0) {
  cat("PASS: Every customer_id has exactly one city.\n")
} else {
  cat("FAIL: These customer_ids have multiple cities:\n")
  print(id_city_check)
}

# Check same customer_id always has same age
id_age_check <- df_raw %>%
  group_by(customer_id) %>%
  summarise(
    unique_ages = n_distinct(age),
    .groups     = "drop"
  ) %>%
  filter(unique_ages > 1)

if (nrow(id_age_check) == 0) {
  cat("PASS: Every customer_id has exactly one age.\n")
} else {
  cat("FAIL: These customer_ids have multiple ages:\n")
  print(id_age_check)
}

cat("\n══════════════════════════════════════\n")
cat("  4D — STEP 4 SUMMARY\n")
cat("══════════════════════════════════════\n")
cat("Total missing values      :", sum(is.na(df_raw)), "\n")
cat("Full duplicate rows       :", full_dupes, "\n")
cat("Partial duplicate rows    :", nrow(partial_dupes), "\n")
cat("Customer ID issues (name) :", nrow(id_name_check), "\n")
cat("Customer ID issues (city) :", nrow(id_city_check), "\n")
cat("Customer ID issues (age)  :", nrow(id_age_check),  "\n")







# ────────────────────────────────────────────────────────────────
# STEP 5 — Value Range & Business Logic Validation
# ────────────────────────────────────────────────────────────────

cat("══════════════════════════════════════\n")
cat("  5A — VALUE RANGE VALIDATION\n")
cat("══════════════════════════════════════\n")

# ── Age check ─────────────────────────────────────────────────
age_violations <- df_raw %>%
  filter(age < 18 | age > 100)
cat("Age violations (< 18 or > 100)     :",
    nrow(age_violations), "\n")
if (nrow(age_violations) > 0) print(age_violations)

# ── Quantity check ────────────────────────────────────────────
qty_violations <- df_raw %>%
  filter(quantity <= 0)
cat("Quantity violations (<= 0)         :",
    nrow(qty_violations), "\n")
if (nrow(qty_violations) > 0) print(qty_violations)

# ── Unit price check ──────────────────────────────────────────
price_violations <- df_raw %>%
  filter(unit_price <= 0)
cat("Unit price violations (<= 0)       :",
    nrow(price_violations), "\n")
if (nrow(price_violations) > 0) print(price_violations)

# ── Total spend check ─────────────────────────────────────────
spend_violations <- df_raw %>%
  filter(total_spend <= 0)
cat("Total spend violations (<= 0)      :",
    nrow(spend_violations), "\n")
if (nrow(spend_violations) > 0) print(spend_violations)

# ── Future date check ─────────────────────────────────────────
future_dates <- df_raw %>%
  filter(as.Date(substr(purchase_date, 1, 10)) > Sys.Date())
cat("Future date violations             :",
    nrow(future_dates), "\n")
if (nrow(future_dates) > 0) print(future_dates)

# ── Too old date check ────────────────────────────────────────
old_dates <- df_raw %>%
  filter(as.Date(substr(purchase_date, 1, 10)) <
           as.Date("2020-01-01"))
cat("Pre-2020 date violations           :",
    nrow(old_dates), "\n")
if (nrow(old_dates) > 0) print(old_dates)

# ── Mobile number check ───────────────────────────────────────
mobile_violations <- df_raw %>%
  mutate(mob_str = as.character(
    formatC(mobile_number, format = "f",
            digits = 0))) %>%
  filter(nchar(mob_str) != 10)
cat("Mobile number violations (!=10 dig):",
    nrow(mobile_violations), "\n")
if (nrow(mobile_violations) > 0) {
  print(mobile_violations %>%
          select(customer_id, customer_name,
                 mobile_number) %>%
          head(5))
}

cat("\n══════════════════════════════════════\n")
cat("  5B — BUSINESS LOGIC VALIDATION\n")
cat("══════════════════════════════════════\n")

# ── Check: total_spend = quantity x unit_price ────────────────
cat("Checking: total_spend = quantity x unit_price\n\n")

df_logic_check <- df_raw %>%
  mutate(
    expected_spend = round(quantity * unit_price, 2),
    actual_spend   = round(total_spend, 2),
    difference     = round(actual_spend - expected_spend, 2),
    mismatch       = abs(difference) > 1
  )

mismatch_count <- sum(df_logic_check$mismatch)
cat("Total mismatches (diff > Rs 1)     :", mismatch_count, "\n")

if (mismatch_count > 0) {
  cat("\nSample mismatches:\n")
  print(df_logic_check %>%
          filter(mismatch) %>%
          select(customer_id, product_name,
                 quantity, unit_price,
                 actual_spend, expected_spend,
                 difference) %>%
          head(10))
  
  cat("\nMismatch amount stats:\n")
  mismatch_diffs <- df_logic_check %>%
    filter(mismatch) %>%
    pull(difference)
  cat("Min diff  : Rs", round(min(mismatch_diffs),  2), "\n")
  cat("Max diff  : Rs", round(max(mismatch_diffs),  2), "\n")
  cat("Mean diff : Rs", round(mean(mismatch_diffs), 2), "\n")
} else {
  cat("PASS: All total_spend values match quantity x unit_price\n")
}

cat("\n══════════════════════════════════════\n")
cat("  5C — CATEGORY CONSISTENCY CHECK\n")
cat("══════════════════════════════════════\n")

# ── Define expected values ────────────────────────────────────
expected <- list(
  gender           = c("Male", "Female", "Other"),
  customer_segment = c("Regular", "Premium",
                       "VIP", "New Customer"),
  payment_method   = c("Cash", "Credit Card",
                       "Debit Card", "UPI",
                       "Net Banking", "Wallet"),
  channel          = c("In-Store", "Online",
                       "Phone", "Mobile App"),
  product_category = c("Electronics", "Groceries",
                       "Clothing",    "Books",
                       "Furniture",   "Beauty",
                       "Automotive",  "Sports",
                       "Toys",        "Other")
)

all_pass <- TRUE
for (col in names(expected)) {
  actual_vals   <- unique(df_raw[[col]])
  unexpected    <- setdiff(actual_vals, expected[[col]])
  missing_vals  <- setdiff(expected[[col]], actual_vals)
  
  if (length(unexpected) == 0 & length(missing_vals) == 0) {
    cat("PASS:", col, "- All values as expected\n")
  } else {
    all_pass <- FALSE
    if (length(unexpected) > 0) {
      cat("FAIL:", col,
          "- Unexpected values:", unexpected, "\n")
    }
    if (length(missing_vals) > 0) {
      cat("INFO:", col,
          "- Missing expected values:", missing_vals, "\n")
    }
  }
}

cat("\n══════════════════════════════════════\n")
cat("  5D — OUTLIER DETECTION (IQR METHOD)\n")
cat("══════════════════════════════════════\n")

detect_outliers <- function(x, col_name) {
  Q1  <- quantile(x, 0.25, na.rm = TRUE)
  Q3  <- quantile(x, 0.75, na.rm = TRUE)
  IQR <- Q3 - Q1
  low <- Q1 - 1.5 * IQR
  up  <- Q3 + 1.5 * IQR
  
  outliers     <- x[x < low | x > up]
  outlier_pct  <- round(length(outliers) /
                          length(x) * 100, 2)
  
  cat("\n──────────────────────────────────\n")
  cat("Column       :", col_name, "\n")
  cat("Lower fence  :", round(low, 2), "\n")
  cat("Upper fence  :", round(up,  2), "\n")
  cat("Outliers     :", length(outliers),
      paste0("(", outlier_pct, "%)"), "\n")
  cat("Min outlier  :", round(min(outliers), 2), "\n")
  cat("Max outlier  :", round(max(outliers), 2), "\n")
}

num_cols <- c("age", "quantity",
              "unit_price", "total_spend")
for (col in num_cols) {
  detect_outliers(df_raw[[col]], col)
}

cat("\n══════════════════════════════════════\n")
cat("  5E — OUTLIER BOXPLOTS\n")
cat("══════════════════════════════════════\n")

p1 <- ggplot(df_raw, aes(y = age)) +
  geom_boxplot(fill           = "#8E44AD",
               alpha          = 0.7,
               outlier.colour = "#E74C3C",
               outlier.size   = 2) +
  labs(title = "Age", y = "Value", x = "") +
  theme_minimal() +
  theme(axis.text.x  = element_blank(),
        plot.title   = element_text(
          face = "bold", hjust = 0.5))

p2 <- ggplot(df_raw, aes(y = quantity)) +
  geom_boxplot(fill           = "#F39C12",
               alpha          = 0.7,
               outlier.colour = "#E74C3C",
               outlier.size   = 2) +
  labs(title = "Quantity", y = "Value", x = "") +
  theme_minimal() +
  theme(axis.text.x  = element_blank(),
        plot.title   = element_text(
          face = "bold", hjust = 0.5))

p3 <- ggplot(df_raw, aes(y = unit_price)) +
  geom_boxplot(fill           = "#27AE60",
               alpha          = 0.7,
               outlier.colour = "#E74C3C",
               outlier.size   = 2) +
  scale_y_continuous(labels = comma) +
  labs(title = "Unit Price (Rs)", y = "Value", x = "") +
  theme_minimal() +
  theme(axis.text.x  = element_blank(),
        plot.title   = element_text(
          face = "bold", hjust = 0.5))

p4 <- ggplot(df_raw, aes(y = total_spend)) +
  geom_boxplot(fill           = "#4F8EF7",
               alpha          = 0.7,
               outlier.colour = "#E74C3C",
               outlier.size   = 2) +
  scale_y_continuous(labels = comma) +
  labs(title = "Total Spend (Rs)", y = "Value", x = "") +
  theme_minimal() +
  theme(axis.text.x  = element_blank(),
        plot.title   = element_text(
          face = "bold", hjust = 0.5))

grid.arrange(p1, p2, p3, p4,
             ncol = 2,
             top  = "Outlier Detection - Numeric Variables")

cat("\n══════════════════════════════════════\n")
cat("  5F — VALIDATION SUMMARY\n")
cat("══════════════════════════════════════\n")

summary_tbl <- data.frame(
  Check = c(
    "Missing values",
    "Full duplicates",
    "Partial duplicates",
    "Age range (18-100)",
    "Quantity > 0",
    "Unit price > 0",
    "Total spend > 0",
    "Future dates",
    "Pre-2020 dates",
    "Mobile 10 digits",
    "Business logic (spend = qty x price)",
    "Category values consistent"
  ),
  Result = c(
    ifelse(sum(is.na(df_raw)) == 0,
           "PASS", "FAIL"),
    ifelse(full_dupes == 0,
           "PASS", "FAIL"),
    ifelse(nrow(partial_dupes) == 0,
           "PASS - kept as valid",
           paste("INFO -", nrow(partial_dupes),
                 "kept as valid separate txns")),
    ifelse(nrow(age_violations)   == 0,
           "PASS", "FAIL"),
    ifelse(nrow(qty_violations)   == 0,
           "PASS", "FAIL"),
    ifelse(nrow(price_violations) == 0,
           "PASS", "FAIL"),
    ifelse(nrow(spend_violations) == 0,
           "PASS", "FAIL"),
    ifelse(nrow(future_dates)     == 0,
           "PASS", "FAIL"),
    ifelse(nrow(old_dates)        == 0,
           "PASS", "FAIL"),
    ifelse(nrow(mobile_violations)== 0,
           "PASS", "FAIL"),
    ifelse(mismatch_count         == 0,
           "PASS", "FAIL"),
    ifelse(all_pass,
           "PASS", "FAIL")
  ),
  row.names = NULL
)

print(summary_tbl)





# ────────────────────────────────────────────────────────────────
# STEP 6 — Data Cleaning
# ────────────────────────────────────────────────────────────────

cat("══════════════════════════════════════\n")
cat("  6A — CREATE WORKING COPY\n")
cat("══════════════════════════════════════\n")

# ── Always clean a COPY, never touch df_raw ───────────────────
df <- df_raw

cat("Working copy created.\n")
cat("Rows    :", nrow(df), "\n")
cat("Columns :", ncol(df), "\n")

cat("\n══════════════════════════════════════\n")
cat("  6B — FIX COLUMN NAMES (snake_case)\n")
cat("══════════════════════════════════════\n")

df <- df %>% clean_names()

cat("Before → After column names:\n")
for (i in seq_along(colnames(df))) {
  cat(sprintf("  %-20s → %s\n",
              colnames(df_raw)[i],
              colnames(df)[i]))
}

cat("\n══════════════════════════════════════\n")
cat("  6C — FIX DATA TYPES\n")
cat("══════════════════════════════════════\n")

cat("Before fixing types:\n")
print(sapply(df, class))

df <- df %>%
  mutate(
    # DateTime — parse properly
    purchase_date    = ymd_hms(purchase_date),
    
    # Integer
    age              = as.integer(age),
    quantity         = as.integer(quantity),
    
    # Numeric
    unit_price       = as.numeric(unit_price),
    total_spend      = as.numeric(total_spend),
    
    # Character → kept as char (ID fields)
    customer_id      = as.character(customer_id),
    customer_name    = trimws(customer_name),
    product_name     = trimws(product_name),
    
    # Mobile → character (not numeric!)
    mobile_number    = as.character(
      formatC(mobile_number,
              format = "f", digits = 0)),
    
    # Factors
    gender           = as.factor(trimws(gender)),
    city             = as.factor(trimws(city)),
    product_category = as.factor(
      trimws(product_category)),
    payment_method   = as.factor(
      trimws(payment_method)),
    channel          = as.factor(trimws(channel)),
    customer_segment = as.factor(
      trimws(customer_segment))
  )

cat("\nAfter fixing types:\n")
print(sapply(df, class))

cat("\nDate column check:\n")
cat("Class    :", class(df$purchase_date), "\n")
cat("Sample   :", format(head(df$purchase_date, 3)), "\n")

cat("\nMobile number check:\n")
cat("Class    :", class(df$mobile_number), "\n")
cat("Sample   :", head(df$mobile_number, 3), "\n")
cat("Nchar    :", 
    paste(nchar(head(df$mobile_number, 3)),
          collapse = ", "), "\n")

cat("\n══════════════════════════════════════\n")
cat("  6D — REMOVE FULL DUPLICATES\n")
cat("══════════════════════════════════════\n")

rows_before <- nrow(df)
df          <- df %>% distinct()
rows_after  <- nrow(df)

cat("Rows before :", rows_before, "\n")
cat("Rows after  :", rows_after,  "\n")
cat("Removed     :", rows_before - rows_after, "\n")

cat("\n══════════════════════════════════════\n")
cat("  6E — RECALCULATE total_spend\n")
cat("══════════════════════════════════════\n")

# ── Recalculate to ensure mathematical consistency ─────────────
df <- df %>%
  mutate(total_spend = round(quantity * unit_price, 2))

cat("total_spend recalculated as quantity x unit_price.\n")
cat("Sample check:\n")
print(df %>%
        select(customer_id, product_name,
               quantity, unit_price, total_spend) %>%
        head(5))

cat("\n══════════════════════════════════════\n")
cat("  6F — CAP OUTLIERS (WINSORIZE 1-99%)\n")
cat("══════════════════════════════════════\n")

winsorize <- function(x, low_pct  = 0.01,
                      high_pct = 0.99) {
  q_low  <- quantile(x, low_pct,  na.rm = TRUE)
  q_high <- quantile(x, high_pct, na.rm = TRUE)
  pmax(pmin(x, q_high), q_low)
}

# ── Before capping ─────────────────────────────────────────────
cat("BEFORE capping:\n")
cat("unit_price  → Min: Rs",
    round(min(df$unit_price),  0),
    " Max: Rs",
    format(round(max(df$unit_price),  0),
           big.mark = ","), "\n")
cat("total_spend → Min: Rs",
    round(min(df$total_spend), 0),
    " Max: Rs",
    format(round(max(df$total_spend), 0),
           big.mark = ","), "\n")

# ── Apply winsorize ────────────────────────────────────────────
df <- df %>%
  mutate(
    unit_price  = winsorize(unit_price),
    total_spend = winsorize(total_spend)
  )

# ── After capping ──────────────────────────────────────────────
cat("\nAFTER capping:\n")
cat("unit_price  → Min: Rs",
    round(min(df$unit_price),  0),
    " Max: Rs",
    format(round(max(df$unit_price),  0),
           big.mark = ","), "\n")
cat("total_spend → Min: Rs",
    round(min(df$total_spend), 0),
    " Max: Rs",
    format(round(max(df$total_spend), 0),
           big.mark = ","), "\n")

cat("\n══════════════════════════════════════\n")
cat("  6G — FINAL CLEAN DATASET CHECK\n")
cat("══════════════════════════════════════\n")

cat("Final dimensions:\n")
cat("  Rows    :", nrow(df), "\n")
cat("  Columns :", ncol(df), "\n")

cat("\nMissing values after cleaning:",
    sum(is.na(df)), "\n")

cat("\nData types after cleaning:\n")
print(sapply(df, class))

cat("\nSample of clean data:\n")
print(head(df, 5))

cat("\n══════════════════════════════════════\n")
cat("  6H — CLEANING SUMMARY\n")
cat("══════════════════════════════════════\n")

cleaning_summary <- data.frame(
  Step   = c(
    "1. Fix column names",
    "2. Fix data types",
    "3. mobile_number to character",
    "4. purchase_date to POSIXct",
    "5. Categories to factor",
    "6. Remove full duplicates",
    "7. Recalculate total_spend",
    "8. Winsorize unit_price (1-99%)",
    "8. Winsorize total_spend (1-99%)"
  ),
  Action = c(
    "Applied clean_names() - snake_case",
    "age & quantity to integer, prices to numeric",
    "Stored as character preserving leading digits",
    "Parsed with ymd_hms()",
    "gender, city, segment, payment, channel, category",
    paste(rows_before - rows_after, "rows removed"),
    "quantity x unit_price rounded to 2 decimal",
    paste("Capped at Rs",
          round(quantile(df_raw$unit_price,  0.01), 0),
          "to Rs",
          format(round(
            quantile(df_raw$unit_price, 0.99), 0),
            big.mark = ",")),
    paste("Capped at Rs",
          round(quantile(df_raw$total_spend, 0.01), 0),
          "to Rs",
          format(round(
            quantile(df_raw$total_spend, 0.99), 0),
            big.mark = ","))
  ),
  row.names = NULL
)

print(cleaning_summary)

cat("\nCleaning COMPLETE.\n")
cat("Clean dataset stored in: df\n")
cat("Raw dataset preserved in: df_raw\n")



# ────────────────────────────────────────────────────────────────
# STEP 7 — Feature Engineering
# ────────────────────────────────────────────────────────────────

cat("══════════════════════════════════════\n")
cat("  7A — DATE & TIME FEATURES\n")
cat("══════════════════════════════════════\n")

df <- df %>%
  mutate(
    year         = as.integer(year(purchase_date)),
    month_num    = as.integer(month(purchase_date)),
    month_name   = month(purchase_date,
                         label = TRUE, abbr = TRUE),
    day          = as.integer(day(purchase_date)),
    hour         = as.integer(hour(purchase_date)),
    day_of_week  = wday(purchase_date,
                        label = TRUE, abbr = TRUE),
    quarter      = paste0("Q",
                          quarter(purchase_date)),
    is_weekend   = wday(purchase_date) %in% c(1, 7),
    is_month_end = day(purchase_date) >= 25,
    
    season = case_when(
      month(purchase_date) %in% c(12, 1, 2)   ~ "Winter",
      month(purchase_date) %in% c(3, 4, 5)    ~ "Summer",
      month(purchase_date) %in% c(6, 7, 8, 9) ~ "Monsoon",
      TRUE                                      ~ "Autumn"
    ),
    
    time_of_day = case_when(
      hour(purchase_date) < 12 ~ "Morning",
      hour(purchase_date) < 15 ~ "Afternoon",
      hour(purchase_date) < 18 ~ "Evening",
      TRUE                     ~ "Night"
    )
  )

cat("Date & time features created:\n")
cat("year, month_num, month_name, day, hour\n")
cat("day_of_week, quarter, is_weekend\n")
cat("is_month_end, season, time_of_day\n")

cat("\nYear distribution:\n")
print(table(df$year))

cat("\nSeason distribution:\n")
print(table(df$season))

cat("\nTime of day distribution:\n")
print(table(df$time_of_day))

cat("\nWeekend vs Weekday:\n")
print(table(df$is_weekend))

cat("\n══════════════════════════════════════\n")
cat("  7B — AGE GROUP FEATURE\n")
cat("══════════════════════════════════════\n")

df <- df %>%
  mutate(
    age_group = cut(
      age,
      breaks = c(17, 25, 35, 45, 55, 100),
      labels = c("18-25", "26-35",
                 "36-45", "46-55", "55+"),
      right  = TRUE
    )
  )

cat("Age group distribution:\n")
age_grp_tbl <- table(df$age_group)
age_grp_pct <- round(prop.table(age_grp_tbl) * 100, 1)
age_grp_df  <- data.frame(
  Age_Group = names(age_grp_tbl),
  Count     = as.integer(age_grp_tbl),
  Percent   = paste0(as.numeric(age_grp_pct), "%"),
  row.names = NULL
)
print(age_grp_df)

cat("\n══════════════════════════════════════\n")
cat("  7C — SPEND TIER FEATURE\n")
cat("══════════════════════════════════════\n")

spend_q <- quantile(df$total_spend,
                    probs = c(0.33, 0.67),
                    na.rm = TRUE)
cat("Spend tier breakpoints:\n")
cat("  Low-Medium boundary  : Rs",
    round(spend_q[1], 0), "\n")
cat("  Medium-High boundary : Rs",
    round(spend_q[2], 0), "\n")

df <- df %>%
  mutate(
    spend_tier = case_when(
      total_spend <= spend_q[1] ~ "Low Spender",
      total_spend <= spend_q[2] ~ "Mid Spender",
      TRUE                       ~ "High Spender"
    ),
    spend_tier = factor(spend_tier,
                        levels = c("Low Spender",
                                   "Mid Spender",
                                   "High Spender"))
  )

cat("\nSpend tier distribution:\n")
print(table(df$spend_tier))

cat("\n══════════════════════════════════════\n")
cat("  7D — LOG TRANSFORM FEATURES\n")
cat("══════════════════════════════════════\n")

# ── Log transform for highly skewed columns ────────────────────
df <- df %>%
  mutate(
    log_unit_price  = round(log1p(unit_price),  4),
    log_total_spend = round(log1p(total_spend), 4)
  )

cat("Log-transformed features created:\n")
cat("log_unit_price  sample:",
    round(head(df$log_unit_price,  5), 2), "\n")
cat("log_total_spend sample:",
    round(head(df$log_total_spend, 5), 2), "\n")

cat("\nSkewness comparison:\n")
cat(sprintf("%-20s original: %6.2f  log: %6.2f\n",
            "unit_price",
            skewness(df$unit_price,      na.rm = TRUE),
            skewness(df$log_unit_price,  na.rm = TRUE)))
cat(sprintf("%-20s original: %6.2f  log: %6.2f\n",
            "total_spend",
            skewness(df$total_spend,     na.rm = TRUE),
            skewness(df$log_total_spend, na.rm = TRUE)))

cat("\n══════════════════════════════════════\n")
cat("  7E — VERIFY FINAL COLUMNS\n")
cat("══════════════════════════════════════\n")

cat("Total columns after feature engineering:",
    ncol(df), "\n\n")

col_info <- data.frame(
  Column = colnames(df),
  Type   = sapply(df, function(x) class(x)[1]),
  row.names = NULL
)
print(col_info)

cat("\nNew features added:\n")
new_features <- c("year", "month_num", "month_name",
                  "day", "hour", "day_of_week",
                  "quarter", "is_weekend",
                  "is_month_end", "season",
                  "time_of_day", "age_group",
                  "spend_tier", "log_unit_price",
                  "log_total_spend")
cat(paste(new_features, collapse = ", "), "\n")
cat("Total new features:", length(new_features), "\n")

cat("\nSample of enriched dataset (first 3 rows):\n")
print(df %>%
        select(customer_id, purchase_date,
               year, month_name, day_of_week,
               season, time_of_day, age_group,
               spend_tier, log_total_spend) %>%
        head(3))




# ────────────────────────────────────────────────────────────────
# STEP 8 — Customer Profiling & RFM Scoring
# ────────────────────────────────────────────────────────────────

cat("══════════════════════════════════════\n")
cat("  8A — CUSTOMER LEVEL AGGREGATION\n")
cat("══════════════════════════════════════\n")

# ── Reference date = 1 day after last purchase ─────────────────
ref_date <- max(df$purchase_date) + days(1)
cat("Reference date for Recency:", 
    format(ref_date, "%Y-%m-%d"), "\n\n")

# ── Build customer profile ─────────────────────────────────────
customer_profile <- df %>%
  group_by(customer_id, customer_name,
           city, gender,
           customer_segment, age, age_group) %>%
  summarise(
    # Recency
    last_purchase_date  = max(purchase_date),
    recency_days        = as.numeric(
      ref_date - max(purchase_date)),
    
    # Frequency
    total_transactions  = n(),
    unique_products     = n_distinct(product_name),
    unique_categories   = n_distinct(product_category),
    
    # Monetary
    total_revenue       = sum(total_spend),
    avg_spend_per_visit = round(mean(total_spend), 2),
    max_single_spend    = max(total_spend),
    min_single_spend    = min(total_spend),
    median_spend        = median(total_spend),
    
    # Preferences
    favorite_category   = names(sort(
      table(product_category),
      decreasing = TRUE))[1],
    favorite_payment    = names(sort(
      table(payment_method),
      decreasing = TRUE))[1],
    favorite_channel    = names(sort(
      table(channel),
      decreasing = TRUE))[1],
    most_active_season  = names(sort(
      table(season),
      decreasing = TRUE))[1],
    most_active_day     = names(sort(
      table(day_of_week),
      decreasing = TRUE))[1],
    most_active_hour    = names(sort(
      table(time_of_day),
      decreasing = TRUE))[1],
    
    .groups = "drop"
  ) %>%
  arrange(customer_id)

cat("Customer profiles built:\n")
cat("  Customers :", nrow(customer_profile), "\n")
cat("  Columns   :", ncol(customer_profile), "\n")

cat("\nSample profile (first 3 customers):\n")
print(customer_profile %>%
        select(customer_id, customer_name,
               recency_days, total_transactions,
               total_revenue, avg_spend_per_visit,
               favorite_category) %>%
        head(3))

cat("\n══════════════════════════════════════\n")
cat("  8B — PURCHASE GAP ANALYSIS\n")
cat("══════════════════════════════════════\n")

# ── Days between consecutive purchases per customer ────────────
purchase_gaps <- df %>%
  arrange(customer_id, purchase_date) %>%
  group_by(customer_id) %>%
  mutate(
    prev_date = lag(purchase_date),
    gap_days  = as.numeric(
      difftime(purchase_date, prev_date,
               units = "days"))
  ) %>%
  summarise(
    avg_days_between  = round(mean(gap_days,
                                   na.rm = TRUE), 1),
    min_gap_days      = round(min(gap_days,
                                  na.rm = TRUE), 1),
    max_gap_days      = round(max(gap_days,
                                  na.rm = TRUE), 1),
    .groups = "drop"
  )

cat("Purchase gap stats (across all customers):\n")
cat("  Avg gap between purchases:\n")
cat("  Min :", round(min(purchase_gaps$avg_days_between,
                         na.rm = TRUE), 1), "days\n")
cat("  Max :", round(max(purchase_gaps$avg_days_between,
                         na.rm = TRUE), 1), "days\n")
cat("  Mean:", round(mean(purchase_gaps$avg_days_between,
                          na.rm = TRUE), 1), "days\n")

# ── Join gaps to profile ───────────────────────────────────────
customer_profile <- customer_profile %>%
  left_join(purchase_gaps, by = "customer_id")

cat("\nPurchase gaps joined to profiles.\n")

cat("\n══════════════════════════════════════\n")
cat("  8C — RFM SCORING\n")
cat("══════════════════════════════════════\n")

cat("Scoring method: quintile scoring (1-5)\n")
cat("  R = 5 means purchased very recently\n")
cat("  F = 5 means purchases most frequently\n")
cat("  M = 5 means highest total spend\n\n")

customer_profile <- customer_profile %>%
  mutate(
    R_score   = ntile(-recency_days,    5),
    F_score   = ntile(total_transactions, 5),
    M_score   = ntile(total_revenue,    5),
    RFM_score = R_score + F_score + M_score
  )

cat("RFM score distribution:\n")
print(table(customer_profile$RFM_score))

cat("\nR_score distribution:\n")
print(table(customer_profile$R_score))

cat("\nF_score distribution:\n")
print(table(customer_profile$F_score))

cat("\nM_score distribution:\n")
print(table(customer_profile$M_score))

cat("\n══════════════════════════════════════\n")
cat("  8D — RFM SEGMENT LABELS\n")
cat("══════════════════════════════════════\n")

customer_profile <- customer_profile %>%
  mutate(
    rfm_segment = case_when(
      RFM_score >= 13                       ~ "Champions",
      RFM_score >= 10                       ~ "Loyal Customers",
      RFM_score >= 7                        ~ "Potential Loyalists",
      R_score   >= 4                        ~ "New Customers",
      F_score   >= 3 & M_score >= 3         ~ "At Risk",
      TRUE                                  ~ "Lost"
    )
  )

cat("RFM Segment distribution:\n")
seg_tbl <- sort(table(customer_profile$rfm_segment),
                decreasing = TRUE)
seg_pct <- round(prop.table(seg_tbl) * 100, 1)
seg_df  <- data.frame(
  Segment = names(seg_tbl),
  Count   = as.integer(seg_tbl),
  Percent = paste0(as.numeric(seg_pct), "%"),
  row.names = NULL
)
print(seg_df)

cat("\n══════════════════════════════════════\n")
cat("  8E — FREQUENCY LABEL\n")
cat("══════════════════════════════════════\n")

customer_profile <- customer_profile %>%
  mutate(
    frequency_label = case_when(
      avg_days_between <= 7   ~ "Weekly Buyer",
      avg_days_between <= 15  ~ "Bi-Weekly Buyer",
      avg_days_between <= 30  ~ "Monthly Buyer",
      avg_days_between <= 60  ~ "Occasional Buyer",
      TRUE                    ~ "Rare Buyer"
    )
  )

cat("Frequency label distribution:\n")
print(sort(table(customer_profile$frequency_label),
           decreasing = TRUE))

cat("\n══════════════════════════════════════\n")
cat("  8F — PREDICT NEXT PURCHASE DATE\n")
cat("══════════════════════════════════════\n")

customer_profile <- customer_profile %>%
  mutate(
    predicted_next_purchase = last_purchase_date +
      days(round(avg_days_between)),
    days_until_next         = as.numeric(
      difftime(predicted_next_purchase,
               Sys.time(), units = "days"))
  )

cat("Predicted next purchase dates calculated.\n\n")
cat("Sample predictions:\n")
print(customer_profile %>%
        select(customer_id, customer_name,
               last_purchase_date,
               avg_days_between,
               predicted_next_purchase,
               days_until_next) %>%
        head(5))

cat("\n══════════════════════════════════════\n")
cat("  8G — MONTHLY SPEND PER CUSTOMER\n")
cat("══════════════════════════════════════\n")

monthly_spend <- df %>%
  group_by(customer_id, year, month_num) %>%
  summarise(
    monthly_total  = sum(total_spend),
    monthly_orders = n(),
    .groups        = "drop"
  )

avg_monthly <- monthly_spend %>%
  group_by(customer_id) %>%
  summarise(
    avg_monthly_spend  = round(mean(monthly_total), 2),
    total_active_months = n(),
    .groups            = "drop"
  )

customer_profile <- customer_profile %>%
  left_join(avg_monthly, by = "customer_id")

cat("Monthly spend stats:\n")
cat("  Overall avg monthly spend per customer: Rs",
    format(round(mean(avg_monthly$avg_monthly_spend,
                      na.rm = TRUE), 0),
           big.mark = ","), "\n")
cat("  Min monthly spend: Rs",
    format(round(min(avg_monthly$avg_monthly_spend,
                     na.rm = TRUE), 0),
           big.mark = ","), "\n")
cat("  Max monthly spend: Rs",
    format(round(max(avg_monthly$avg_monthly_spend,
                     na.rm = TRUE), 0),
           big.mark = ","), "\n")

cat("\n══════════════════════════════════════\n")
cat("  8H — CUSTOMER PROFILE SUMMARY\n")
cat("══════════════════════════════════════\n")

cat("Final customer profile:\n")
cat("  Rows    :", nrow(customer_profile), "\n")
cat("  Columns :", ncol(customer_profile), "\n")

cat("\nAll columns in customer_profile:\n")
print(colnames(customer_profile))

cat("\nTop 5 customers by total revenue:\n")
print(customer_profile %>%
        arrange(desc(total_revenue)) %>%
        select(customer_id, customer_name,
               total_transactions,
               total_revenue, rfm_segment,
               frequency_label) %>%
        head(5))

cat("\nRFM segment vs customer_segment cross-check:\n")
print(table(customer_profile$customer_segment,
            customer_profile$rfm_segment))


# ────────────────────────────────────────────────────────────────
# STEP 9 — EDA Visualizations
# ────────────────────────────────────────────────────────────────

# ── Common theme ───────────────────────────────────────────────
theme_sales <- theme_minimal(base_size = 12) +
  theme(
    plot.title      = element_text(
      face  = "bold", hjust = 0.5, size = 13),
    plot.subtitle   = element_text(
      hjust = 0.5, color = "grey50"),
    axis.text       = element_text(size = 10),
    legend.position = "bottom"
  )

cat("══════════════════════════════════════\n")
cat("  9A — MONTHLY REVENUE TREND\n")
cat("══════════════════════════════════════\n")

monthly_trend <- df %>%
  mutate(year_month = floor_date(
    purchase_date, "month")) %>%
  group_by(year_month) %>%
  summarise(
    revenue = sum(total_spend),
    orders  = n(),
    .groups = "drop"
  )

ggplot(monthly_trend,
       aes(x = year_month, y = revenue)) +
  geom_line(color = "#4F8EF7",
            linewidth = 1.2) +
  geom_point(color = "#4F8EF7", size = 2.5) +
  geom_smooth(method = "loess",
              se     = TRUE,
              color  = "#E74C3C",
              fill   = "#E74C3C",
              alpha  = 0.15) +
  scale_y_continuous(
    labels = function(x)
      paste0("Rs ", format(x / 1e6,
                           big.mark = ","),
             "M")) +
  scale_x_datetime(date_labels = "%b %Y",
                   date_breaks = "2 months") +
  labs(
    title    = "Monthly Revenue Trend",
    subtitle = "Jan 2023 – Mar 2024",
    x        = "Month",
    y        = "Revenue"
  ) +
  theme_sales +
  theme(axis.text.x = element_text(
    angle = 45, hjust = 1))

cat("Plot 9A done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9B — REVENUE BY DAY OF WEEK\n")
cat("══════════════════════════════════════\n")

dow_rev <- df %>%
  group_by(day_of_week) %>%
  summarise(
    revenue = sum(total_spend),
    orders  = n(),
    .groups = "drop"
  )

ggplot(dow_rev,
       aes(x    = day_of_week,
           y    = revenue,
           fill = day_of_week)) +
  geom_col(show.legend = FALSE,
           width = 0.7) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    vjust = -0.5, size = 3.5,
    fontface = "bold") +
  scale_fill_brewer(palette = "Set2") +
  scale_y_continuous(
    labels = function(x)
      paste0("Rs ", round(x / 1e6, 1), "M")) +
  labs(
    title    = "Revenue by Day of Week",
    subtitle = "Which day drives most sales?",
    x        = "Day",
    y        = "Revenue"
  ) +
  theme_sales

cat("Plot 9B done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9C — REVENUE BY QUARTER\n")
cat("══════════════════════════════════════\n")

df %>%
  group_by(quarter) %>%
  summarise(
    revenue = sum(total_spend),
    orders  = n(),
    .groups = "drop"
  ) %>%
  ggplot(aes(x    = quarter,
             y    = revenue,
             fill = quarter)) +
  geom_col(show.legend = FALSE,
           width = 0.6) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M\n(",
      orders, " orders)")),
    vjust = -0.4, size = 3.5) +
  scale_fill_manual(
    values = c("#3498DB", "#E67E22",
               "#2ECC71", "#9B59B6")) +
  scale_y_continuous(
    labels = function(x)
      paste0("Rs ", round(x / 1e6, 1), "M")) +
  labs(
    title    = "Revenue by Quarter",
    subtitle = "Quarterly performance overview",
    x        = "Quarter",
    y        = "Revenue"
  ) +
  theme_sales

cat("Plot 9C done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9D — REVENUE BY SEASON\n")
cat("══════════════════════════════════════\n")

season_order <- c("Winter", "Summer",
                  "Monsoon", "Autumn")

df %>%
  mutate(season = factor(season,
                         levels = season_order)) %>%
  group_by(season) %>%
  summarise(
    revenue  = sum(total_spend),
    orders   = n(),
    avg_spend = round(mean(total_spend), 0),
    .groups  = "drop"
  ) %>%
  ggplot(aes(x    = season,
             y    = revenue,
             fill = season)) +
  geom_col(show.legend = FALSE,
           width = 0.6) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    vjust = -0.5, size = 3.8,
    fontface = "bold") +
  scale_fill_manual(
    values = c("#74B9FF", "#FDCB6E",
               "#55EFC4", "#A29BFE")) +
  scale_y_continuous(
    labels = function(x)
      paste0("Rs ", round(x / 1e6, 1), "M")) +
  labs(
    title    = "Revenue by Season",
    subtitle = "Which season has highest sales?",
    x        = "Season",
    y        = "Total Revenue"
  ) +
  theme_sales

cat("Plot 9D done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9E — TOP 10 PRODUCT CATEGORIES\n")
cat("══════════════════════════════════════\n")

cat_summary <- df %>%
  group_by(product_category) %>%
  summarise(
    revenue    = sum(total_spend),
    orders     = n(),
    avg_spend  = round(mean(total_spend), 0),
    .groups    = "drop"
  ) %>%
  arrange(desc(revenue))

print(cat_summary)

ggplot(cat_summary,
       aes(x    = reorder(
         product_category, revenue),
         y    = revenue,
         fill = product_category)) +
  geom_col(show.legend = FALSE) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    hjust = -0.1, size = 3.5) +
  coord_flip() +
  scale_fill_brewer(palette = "Paired") +
  scale_x_discrete() +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.15)),
    labels = function(x)
      paste0("Rs ", round(x / 1e6, 1), "M")) +
  labs(
    title    = "Revenue by Product Category",
    subtitle = "Top performing categories",
    x        = "Category",
    y        = "Total Revenue"
  ) +
  theme_sales

cat("Plot 9E done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9F — CUSTOMER SEGMENT ANALYSIS\n")
cat("══════════════════════════════════════\n")

seg_summary <- df %>%
  group_by(customer_segment) %>%
  summarise(
    revenue    = sum(total_spend),
    orders     = n(),
    customers  = n_distinct(customer_id),
    avg_spend  = round(mean(total_spend), 0),
    .groups    = "drop"
  )

print(seg_summary)

p_seg1 <- ggplot(
  seg_summary,
  aes(x    = reorder(
    customer_segment, revenue),
    y    = revenue,
    fill = customer_segment)) +
  geom_col(show.legend = FALSE) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    hjust = -0.1, size = 3.5) +
  coord_flip() +
  scale_fill_manual(
    values = c("#E74C3C", "#F39C12",
               "#27AE60", "#3498DB")) +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.2))) +
  labs(title = "Revenue by Segment",
       x = "", y = "Revenue") +
  theme_sales

p_seg2 <- ggplot(
  seg_summary,
  aes(x    = reorder(
    customer_segment, avg_spend),
    y    = avg_spend,
    fill = customer_segment)) +
  geom_col(show.legend = FALSE) +
  geom_text(
    aes(label = paste0(
      "Rs ", format(avg_spend,
                    big.mark = ","))),
    hjust = -0.1, size = 3.5) +
  coord_flip() +
  scale_fill_manual(
    values = c("#E74C3C", "#F39C12",
               "#27AE60", "#3498DB")) +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.2))) +
  labs(title = "Avg Spend by Segment",
       x = "", y = "Avg Spend") +
  theme_sales

grid.arrange(p_seg1, p_seg2, ncol = 2)
cat("Plot 9F done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9G — GENDER & AGE ANALYSIS\n")
cat("══════════════════════════════════════\n")

p_gender <- df %>%
  group_by(gender) %>%
  summarise(
    revenue   = sum(total_spend),
    orders    = n(),
    avg_spend = round(mean(total_spend), 0),
    .groups   = "drop"
  ) %>%
  ggplot(aes(x    = gender,
             y    = revenue,
             fill = gender)) +
  geom_col(show.legend = FALSE,
           width = 0.6) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    vjust = -0.5, size = 3.5) +
  scale_fill_manual(
    values = c("#E91E8C", "#3498DB",
               "#27AE60")) +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.15))) +
  labs(title    = "Revenue by Gender",
       x = "Gender", y = "Revenue") +
  theme_sales

p_age <- df %>%
  group_by(age_group) %>%
  summarise(
    revenue   = sum(total_spend),
    orders    = n(),
    avg_spend = round(mean(total_spend), 0),
    .groups   = "drop"
  ) %>%
  ggplot(aes(x    = age_group,
             y    = revenue,
             fill = age_group)) +
  geom_col(show.legend = FALSE,
           width = 0.6) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    vjust = -0.5, size = 3.5) +
  scale_fill_brewer(palette = "Set1") +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.15))) +
  labs(title    = "Revenue by Age Group",
       x = "Age Group", y = "Revenue") +
  theme_sales

grid.arrange(p_gender, p_age, ncol = 2)
cat("Plot 9G done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9H — PAYMENT METHOD & CHANNEL\n")
cat("══════════════════════════════════════\n")

p_pay <- df %>%
  group_by(payment_method) %>%
  summarise(
    orders    = n(),
    revenue   = sum(total_spend),
    .groups   = "drop"
  ) %>%
  mutate(pct = round(orders /
                       sum(orders) * 100, 1)) %>%
  ggplot(aes(x    = reorder(
    payment_method, orders),
    y    = orders,
    fill = payment_method)) +
  geom_col(show.legend = FALSE) +
  geom_text(
    aes(label = paste0(pct, "%")),
    hjust = -0.2, size = 3.5) +
  coord_flip() +
  scale_fill_brewer(palette = "Set3") +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.15))) +
  labs(title = "Orders by Payment Method",
       x = "", y = "Orders") +
  theme_sales

p_chan <- df %>%
  group_by(channel) %>%
  summarise(
    revenue = sum(total_spend),
    orders  = n(),
    .groups = "drop"
  ) %>%
  ggplot(aes(x    = reorder(
    channel, revenue),
    y    = revenue,
    fill = channel)) +
  geom_col(show.legend = FALSE) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    hjust = -0.1, size = 3.5) +
  coord_flip() +
  scale_fill_manual(
    values = c("#FF6B6B", "#4ECDC4",
               "#45B7D1", "#96CEB4")) +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.2))) +
  labs(title = "Revenue by Channel",
       x = "", y = "Revenue") +
  theme_sales

grid.arrange(p_pay, p_chan, ncol = 2)
cat("Plot 9H done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9I — CITY REVENUE MAP\n")
cat("══════════════════════════════════════\n")

df %>%
  group_by(city) %>%
  summarise(
    revenue   = sum(total_spend),
    customers = n_distinct(customer_id),
    orders    = n(),
    avg_spend = round(mean(total_spend), 0),
    .groups   = "drop"
  ) %>%
  arrange(desc(revenue)) %>%
  ggplot(aes(x    = reorder(city, revenue),
             y    = revenue,
             fill = revenue)) +
  geom_col(show.legend = FALSE) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    hjust = -0.1, size = 3.5) +
  coord_flip() +
  scale_fill_gradient(
    low  = "#AED6F1",
    high = "#1A5276") +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.2))) +
  labs(
    title    = "Revenue by City",
    subtitle = "Top performing cities",
    x        = "City",
    y        = "Total Revenue"
  ) +
  theme_sales

cat("Plot 9I done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9J — RFM SEGMENT DISTRIBUTION\n")
cat("══════════════════════════════════════\n")

customer_profile %>%
  count(rfm_segment) %>%
  mutate(pct = round(n / sum(n) * 100, 1)) %>%
  ggplot(aes(x    = reorder(rfm_segment, n),
             y    = n,
             fill = rfm_segment)) +
  geom_col(show.legend = FALSE,
           width = 0.7) +
  geom_text(
    aes(label = paste0(n, " (", pct, "%)")),
    hjust = -0.1, size = 3.8,
    fontface = "bold") +
  coord_flip() +
  scale_fill_manual(
    values = c(
      "Champions"           = "#2ECC71",
      "Loyal Customers"     = "#3498DB",
      "Potential Loyalists" = "#F39C12",
      "New Customers"       = "#9B59B6",
      "At Risk"             = "#E67E22",
      "Lost"                = "#E74C3C"
    )) +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.2))) +
  labs(
    title    = "RFM Customer Segments",
    subtitle = "Based on Recency, Frequency, Monetary scoring",
    x        = "Segment",
    y        = "Number of Customers"
  ) +
  theme_sales

cat("Plot 9J done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9K — SPEND DISTRIBUTION\n")
cat("══════════════════════════════════════\n")

p_hist <- ggplot(df,
                 aes(x = log_total_spend)) +
  geom_histogram(
    fill   = "#3498DB",
    color  = "white",
    bins   = 40,
    alpha  = 0.8) +
  labs(
    title    = "Log(Total Spend) Distribution",
    subtitle = "Log transform applied",
    x        = "log(Total Spend)",
    y        = "Count") +
  theme_sales

p_ridge <- ggplot(
  df,
  aes(x    = log_total_spend,
      y    = product_category,
      fill = product_category)) +
  geom_density_ridges(
    alpha    = 0.7,
    scale    = 1.2,
    show.legend = FALSE) +
  scale_fill_brewer(palette = "Paired") +
  labs(
    title    = "Spend Distribution by Category",
    subtitle = "Ridge plot (log scale)",
    x        = "log(Total Spend)",
    y        = "Category") +
  theme_sales

grid.arrange(p_hist, p_ridge, ncol = 2)
cat("Plot 9K done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9L — CORRELATION HEATMAP\n")
cat("══════════════════════════════════════\n")

num_data <- df %>%
  select(age, quantity,
         unit_price, total_spend,
         log_unit_price,
         log_total_spend) %>%
  na.omit()

corr_mat <- cor(num_data)

ggcorrplot(
  corr_mat,
  method   = "circle",
  type     = "lower",
  lab      = TRUE,
  lab_size = 3.5,
  colors   = c("#E74C3C", "white",
               "#2ECC71"),
  title    = "Correlation Matrix — Numeric Variables",
  ggtheme  = theme_minimal()
)

cat("Plot 9L done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9M — TOP 10 PRODUCTS BY REVENUE\n")
cat("══════════════════════════════════════\n")

top_products <- df %>%
  group_by(product_name, product_category) %>%
  summarise(
    revenue = sum(total_spend),
    orders  = n(),
    .groups = "drop"
  ) %>%
  arrange(desc(revenue)) %>%
  head(10)

print(top_products)

ggplot(top_products,
       aes(x    = reorder(
         product_name, revenue),
         y    = revenue,
         fill = product_category)) +
  geom_col() +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    hjust = -0.1, size = 3.2) +
  coord_flip() +
  scale_fill_brewer(palette = "Set1") +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.25))) +
  labs(
    title    = "Top 10 Products by Revenue",
    subtitle = "Coloured by category",
    x        = "Product",
    y        = "Revenue",
    fill     = "Category"
  ) +
  theme_sales

cat("Plot 9M done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9N — TIME OF DAY vs CHANNEL\n")
cat("══════════════════════════════════════\n")

df %>%
  group_by(time_of_day, channel) %>%
  summarise(
    orders  = n(),
    revenue = sum(total_spend),
    .groups = "drop"
  ) %>%
  mutate(time_of_day = factor(
    time_of_day,
    levels = c("Morning", "Afternoon",
               "Evening", "Night"))) %>%
  ggplot(aes(x    = time_of_day,
             y    = orders,
             fill = channel)) +
  geom_col(position = "dodge") +
  scale_fill_brewer(palette = "Set2") +
  labs(
    title    = "Orders by Time of Day & Channel",
    subtitle = "Which channel is used when?",
    x        = "Time of Day",
    y        = "Number of Orders",
    fill     = "Channel"
  ) +
  theme_sales

cat("Plot 9N done.\n")

cat("\n══════════════════════════════════════\n")
cat("  9O — CATEGORY x PAYMENT HEATMAP\n")
cat("══════════════════════════════════════\n")

df %>%
  group_by(product_category,
           payment_method) %>%
  summarise(
    orders  = n(),
    .groups = "drop"
  ) %>%
  ggplot(aes(x    = payment_method,
             y    = product_category,
             fill = orders)) +
  geom_tile(color = "white",
            linewidth = 0.5) +
  geom_text(aes(label = orders),
            size = 3.5,
            fontface = "bold") +
  scale_fill_gradient(
    low  = "#EBF5FB",
    high = "#1A5276",
    name = "Orders") +
  labs(
    title    = "Product Category vs Payment Method",
    subtitle = "Number of orders per combination",
    x        = "Payment Method",
    y        = "Product Category"
  ) +
  theme_sales +
  theme(axis.text.x = element_text(
    angle = 30, hjust = 1))

cat("Plot 9O done.\n")

cat("\n══════════════════════════════════════\n")
cat("  STEP 9 COMPLETE — ALL PLOTS DONE\n")
cat("══════════════════════════════════════\n")
cat("Plots created: 9A to 9O (15 charts)\n")


# ────────────────────────────────────────────────────────────────
# STEP 10 — Save All Outputs
# ────────────────────────────────────────────────────────────────

cat("══════════════════════════════════════\n")
cat("  10A — CREATE OUTPUT FOLDERS\n")
cat("══════════════════════════════════════\n")

# ── Define output paths ────────────────────────────────────────
output_dir   <- file.path(project_root, "Output")
plots_dir    <- file.path(output_dir,   "Plots")
data_dir     <- file.path(output_dir,   "Data")
reports_dir  <- file.path(output_dir,   "Reports")

# ── Create folders ─────────────────────────────────────────────
for (d in c(output_dir, plots_dir,
            data_dir,   reports_dir)) {
  if (!dir.exists(d)) {
    dir.create(d, recursive = TRUE)
    cat("Created:", d, "\n")
  } else {
    cat("Exists :", d, "\n")
  }
}

cat("\n══════════════════════════════════════\n")
cat("  10B — SAVE CLEAN DATASETS (CSV)\n")
cat("══════════════════════════════════════\n")

# ── Save clean transaction data ────────────────────────────────
clean_path <- file.path(
  data_dir, "clean_sales_data.csv")

write.csv(df,
          file      = clean_path,
          row.names = FALSE)

cat("Saved: clean_sales_data.csv\n")
cat("  Rows    :", nrow(df), "\n")
cat("  Columns :", ncol(df), "\n")
cat("  Size    :",
    round(file.size(clean_path) / 1024, 2),
    "KB\n")

# ── Save customer profile ──────────────────────────────────────
profile_path <- file.path(
  data_dir, "customer_profile.csv")

# Convert list columns / special types before saving
cp_save <- customer_profile %>%
  mutate(
    last_purchase_date      = as.character(
      last_purchase_date),
    predicted_next_purchase = as.character(
      predicted_next_purchase)
  )

write.csv(cp_save,
          file      = profile_path,
          row.names = FALSE)

cat("\nSaved: customer_profile.csv\n")
cat("  Rows    :", nrow(cp_save), "\n")
cat("  Columns :", ncol(cp_save), "\n")
cat("  Size    :",
    round(file.size(profile_path) / 1024, 2),
    "KB\n")

# ── Save monthly trend data ────────────────────────────────────
monthly_path <- file.path(
  data_dir, "monthly_trend.csv")

write.csv(monthly_trend,
          file      = monthly_path,
          row.names = FALSE)

cat("\nSaved: monthly_trend.csv\n")
cat("  Rows :", nrow(monthly_trend), "\n")

# ── Save category summary ──────────────────────────────────────
cat_path <- file.path(
  data_dir, "category_summary.csv")

write.csv(cat_summary,
          file      = cat_path,
          row.names = FALSE)

cat("Saved: category_summary.csv\n")

cat("\n══════════════════════════════════════\n")
cat("  10C — SAVE ALL PLOTS AS PNG\n")
cat("══════════════════════════════════════\n")

save_plot <- function(plot_code,
                      filename,
                      width  = 12,
                      height = 7) {
  path <- file.path(plots_dir, filename)
  png(path,
      width  = width  * 100,
      height = height * 100,
      res    = 100)
  print(plot_code)
  dev.off()
  cat("Saved:", filename, "\n")
}

# ── 9A Monthly Revenue Trend ───────────────────────────────────
p9a <- ggplot(monthly_trend,
              aes(x = year_month,
                  y = revenue)) +
  geom_line(color     = "#4F8EF7",
            linewidth = 1.2) +
  geom_point(color = "#4F8EF7",
             size  = 2.5) +
  geom_smooth(method = "loess",
              se     = TRUE,
              color  = "#E74C3C",
              fill   = "#E74C3C",
              alpha  = 0.15) +
  scale_y_continuous(
    labels = function(x)
      paste0("Rs ",
             round(x / 1e6, 1), "M")) +
  scale_x_datetime(
    date_labels = "%b %Y",
    date_breaks = "2 months") +
  labs(title    = "Monthly Revenue Trend",
       subtitle = "Jan 2023 – Mar 2024",
       x = "Month", y = "Revenue") +
  theme_sales +
  theme(axis.text.x = element_text(
    angle = 45, hjust = 1))

save_plot(p9a, "9A_monthly_revenue_trend.png")

# ── 9B Revenue by Day of Week ──────────────────────────────────
p9b <- ggplot(dow_rev,
              aes(x    = day_of_week,
                  y    = revenue,
                  fill = day_of_week)) +
  geom_col(show.legend = FALSE,
           width = 0.7) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    vjust = -0.5, size = 3.5,
    fontface = "bold") +
  scale_fill_brewer(palette = "Set2") +
  scale_y_continuous(
    labels = function(x)
      paste0("Rs ", round(x / 1e6, 1), "M")) +
  labs(title    = "Revenue by Day of Week",
       subtitle = "Which day drives most sales?",
       x = "Day", y = "Revenue") +
  theme_sales

save_plot(p9b, "9B_revenue_by_day.png")

# ── 9C Revenue by Quarter ──────────────────────────────────────
p9c <- df %>%
  group_by(quarter) %>%
  summarise(
    revenue = sum(total_spend),
    orders  = n(),
    .groups = "drop") %>%
  ggplot(aes(x    = quarter,
             y    = revenue,
             fill = quarter)) +
  geom_col(show.legend = FALSE,
           width = 0.6) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M\n(",
      orders, " orders)")),
    vjust = -0.4, size = 3.5) +
  scale_fill_manual(
    values = c("#3498DB", "#E67E22",
               "#2ECC71", "#9B59B6")) +
  scale_y_continuous(
    labels = function(x)
      paste0("Rs ", round(x / 1e6, 1), "M")) +
  labs(title    = "Revenue by Quarter",
       subtitle = "Quarterly performance overview",
       x = "Quarter", y = "Revenue") +
  theme_sales

save_plot(p9c, "9C_revenue_by_quarter.png")

# ── 9D Revenue by Season ───────────────────────────────────────
p9d <- df %>%
  mutate(season = factor(
    season, levels = season_order)) %>%
  group_by(season) %>%
  summarise(
    revenue  = sum(total_spend),
    orders   = n(),
    avg_spend = round(mean(total_spend), 0),
    .groups  = "drop") %>%
  ggplot(aes(x    = season,
             y    = revenue,
             fill = season)) +
  geom_col(show.legend = FALSE,
           width = 0.6) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    vjust = -0.5, size = 3.8,
    fontface = "bold") +
  scale_fill_manual(
    values = c("#74B9FF", "#FDCB6E",
               "#55EFC4", "#A29BFE")) +
  scale_y_continuous(
    labels = function(x)
      paste0("Rs ", round(x / 1e6, 1), "M")) +
  labs(title    = "Revenue by Season",
       subtitle = "Which season has highest sales?",
       x = "Season", y = "Total Revenue") +
  theme_sales

save_plot(p9d, "9D_revenue_by_season.png")

# ── 9E Category Revenue ────────────────────────────────────────
p9e <- ggplot(cat_summary,
              aes(x    = reorder(
                product_category, revenue),
                y    = revenue,
                fill = product_category)) +
  geom_col(show.legend = FALSE) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    hjust = -0.1, size = 3.5) +
  coord_flip() +
  scale_fill_brewer(palette = "Paired") +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.15)),
    labels = function(x)
      paste0("Rs ", round(x / 1e6, 1), "M")) +
  labs(title    = "Revenue by Product Category",
       subtitle = "Top performing categories",
       x = "Category", y = "Total Revenue") +
  theme_sales

save_plot(p9e, "9E_category_revenue.png")

# ── 9F Segment Analysis ────────────────────────────────────────
p9f <- grid.arrange(p_seg1, p_seg2, ncol = 2)
save_plot(p9f, "9F_segment_analysis.png")

# ── 9G Gender & Age ───────────────────────────────────────────
p9g <- grid.arrange(p_gender, p_age, ncol = 2)
save_plot(p9g, "9G_gender_age_revenue.png")

# ── 9H Payment & Channel ──────────────────────────────────────
p9h <- grid.arrange(p_pay, p_chan, ncol = 2)
save_plot(p9h, "9H_payment_channel.png")

# ── 9I City Revenue ────────────────────────────────────────────
p9i <- df %>%
  group_by(city) %>%
  summarise(
    revenue   = sum(total_spend),
    customers = n_distinct(customer_id),
    orders    = n(),
    avg_spend = round(mean(total_spend), 0),
    .groups   = "drop") %>%
  arrange(desc(revenue)) %>%
  ggplot(aes(x    = reorder(city, revenue),
             y    = revenue,
             fill = revenue)) +
  geom_col(show.legend = FALSE) +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    hjust = -0.1, size = 3.5) +
  coord_flip() +
  scale_fill_gradient(
    low  = "#AED6F1",
    high = "#1A5276") +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.2))) +
  labs(title    = "Revenue by City",
       subtitle = "Top performing cities",
       x = "City", y = "Total Revenue") +
  theme_sales

save_plot(p9i, "9I_city_revenue.png")

# ── 9J RFM Segments ────────────────────────────────────────────
p9j <- customer_profile %>%
  count(rfm_segment) %>%
  mutate(pct = round(n / sum(n) * 100, 1)) %>%
  ggplot(aes(x    = reorder(rfm_segment, n),
             y    = n,
             fill = rfm_segment)) +
  geom_col(show.legend = FALSE,
           width = 0.7) +
  geom_text(
    aes(label = paste0(n, " (", pct, "%)")),
    hjust = -0.1, size = 3.8,
    fontface = "bold") +
  coord_flip() +
  scale_fill_manual(
    values = c(
      "Champions"           = "#2ECC71",
      "Loyal Customers"     = "#3498DB",
      "Potential Loyalists" = "#F39C12",
      "New Customers"       = "#9B59B6",
      "At Risk"             = "#E67E22",
      "Lost"                = "#E74C3C")) +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.2))) +
  labs(
    title    = "RFM Customer Segments",
    subtitle = "Recency, Frequency, Monetary scoring",
    x = "Segment",
    y = "Number of Customers") +
  theme_sales

save_plot(p9j, "9J_rfm_segments.png")

# ── 9K Spend Distribution ──────────────────────────────────────
p9k <- grid.arrange(p_hist, p_ridge, ncol = 2)
save_plot(p9k, "9K_spend_distribution.png",
          width = 14)

# ── 9L Correlation Heatmap ─────────────────────────────────────
p9l <- ggcorrplot(
  corr_mat,
  method   = "circle",
  type     = "lower",
  lab      = TRUE,
  lab_size = 3.5,
  colors   = c("#E74C3C", "white",
               "#2ECC71"),
  title    = "Correlation Matrix — Numeric Variables",
  ggtheme  = theme_minimal())

save_plot(p9l, "9L_correlation_heatmap.png")

# ── 9M Top 10 Products ─────────────────────────────────────────
p9m <- ggplot(
  top_products,
  aes(x    = reorder(product_name, revenue),
      y    = revenue,
      fill = product_category)) +
  geom_col() +
  geom_text(
    aes(label = paste0(
      "Rs ", round(revenue / 1e6, 1), "M")),
    hjust = -0.1, size = 3.2) +
  coord_flip() +
  scale_fill_brewer(palette = "Set1") +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.25))) +
  labs(
    title    = "Top 10 Products by Revenue",
    subtitle = "Coloured by category",
    x = "Product", y = "Revenue",
    fill = "Category") +
  theme_sales

save_plot(p9m, "9M_top10_products.png")

# ── 9N Time of Day vs Channel ──────────────────────────────────
p9n <- df %>%
  group_by(time_of_day, channel) %>%
  summarise(
    orders  = n(),
    revenue = sum(total_spend),
    .groups = "drop") %>%
  mutate(time_of_day = factor(
    time_of_day,
    levels = c("Morning", "Afternoon",
               "Evening", "Night"))) %>%
  ggplot(aes(x    = time_of_day,
             y    = orders,
             fill = channel)) +
  geom_col(position = "dodge") +
  scale_fill_brewer(palette = "Set2") +
  labs(
    title    = "Orders by Time of Day & Channel",
    subtitle = "Which channel is used when?",
    x = "Time of Day",
    y = "Number of Orders",
    fill = "Channel") +
  theme_sales

save_plot(p9n, "9N_time_channel.png")

# ── 9O Category x Payment Heatmap ─────────────────────────────
p9o <- df %>%
  group_by(product_category,
           payment_method) %>%
  summarise(orders  = n(),
            .groups = "drop") %>%
  ggplot(aes(x    = payment_method,
             y    = product_category,
             fill = orders)) +
  geom_tile(color     = "white",
            linewidth = 0.5) +
  geom_text(aes(label   = orders),
            size     = 3.5,
            fontface = "bold") +
  scale_fill_gradient(
    low  = "#EBF5FB",
    high = "#1A5276",
    name = "Orders") +
  labs(
    title    = "Product Category vs Payment Method",
    subtitle = "Number of orders per combination",
    x = "Payment Method",
    y = "Product Category") +
  theme_sales +
  theme(axis.text.x = element_text(
    angle = 30, hjust = 1))

save_plot(p9o, "9O_category_payment_heatmap.png",
          width = 10, height = 7)

cat("\n══════════════════════════════════════\n")
cat("  10D — SAVE SUMMARY REPORT (TXT)\n")
cat("══════════════════════════════════════\n")

report_path <- file.path(
  reports_dir, "analysis_summary.txt")

sink(report_path)
cat("╔══════════════════════════════════════╗\n")
cat("║   SALES DATA ANALYSIS SUMMARY       ║\n")
cat("╚══════════════════════════════════════╝\n")
cat("Generated on:", format(Sys.time()), "\n\n")

cat("── DATASET OVERVIEW ──────────────────\n")
cat("Total rows          :", nrow(df), "\n")
cat("Total columns       :", ncol(df), "\n")
cat("Date range          : 2023-01-01 to 2024-03-30\n")
cat("Unique customers    :", n_distinct(df$customer_id), "\n")
cat("Unique products     :", n_distinct(df$product_name), "\n")
cat("Unique categories   :", n_distinct(df$product_category), "\n")
cat("Cities covered      :", n_distinct(df$city), "\n\n")

cat("── REVENUE SUMMARY ───────────────────\n")
cat("Total Revenue    : Rs",
    format(round(sum(df$total_spend), 0),
           big.mark = ","), "\n")
cat("Avg per txn      : Rs",
    format(round(mean(df$total_spend), 2),
           big.mark = ","), "\n")
cat("Max single txn   : Rs",
    format(round(max(df$total_spend), 0),
           big.mark = ","), "\n")
cat("Min single txn   : Rs",
    format(round(min(df$total_spend), 0),
           big.mark = ","), "\n\n")

cat("── TOP PERFORMERS ────────────────────\n")
cat("Top Category  : Electronics\n")
cat("Top Product   : MacBook Air M2\n")
cat("Top City      : Bangalore\n")
cat("Top Segment   : VIP\n")
cat("Top Channel   : Online\n")
cat("Top Payment   : UPI\n\n")

cat("── RFM SEGMENTS ──────────────────────\n")
print(seg_df)

cat("\n── DATA QUALITY ──────────────────────\n")
cat("Missing values      : 0\n")
cat("Duplicate rows      : 0\n")
cat("Validation checks   : 12/12 PASSED\n")

sink()

cat("Report saved:", report_path, "\n")

cat("\n══════════════════════════════════════\n")
cat("  10E — VERIFY ALL SAVED FILES\n")
cat("══════════════════════════════════════\n")

all_files <- list.files(
  output_dir,
  recursive = TRUE,
  full.names = TRUE)

file_info <- data.frame(
  File     = basename(all_files),
  Folder   = dirname(all_files),
  Size_KB  = round(
    file.size(all_files) / 1024, 1),
  row.names = NULL
)

print(file_info)

cat("\nTotal files saved:", nrow(file_info), "\n")

cat("\n══════════════════════════════════════\n")
cat("  10F — SAVE SUMMARY\n")
cat("══════════════════════════════════════\n")

cat("Folder structure created:\n")
cat("  Output/\n")
cat("  ├── Data/\n")
cat("  │   ├── clean_sales_data.csv\n")
cat("  │   ├── customer_profile.csv\n")
cat("  │   ├── monthly_trend.csv\n")
cat("  │   └── category_summary.csv\n")
cat("  ├── Plots/\n")
cat("  │   ├── 9A_monthly_revenue_trend.png\n")
cat("  │   ├── 9B_revenue_by_day.png\n")
cat("  │   ├── ... (15 plots total)\n")
cat("  │   └── 9O_category_payment_heatmap.png\n")
cat("  └── Reports/\n")
cat("      └── analysis_summary.txt\n")
cat("\nSTEP 10 COMPLETE.\n")

