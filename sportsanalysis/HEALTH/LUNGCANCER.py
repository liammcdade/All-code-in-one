import pandas as pd

# Load your dataset (assumes a CSV file named "lung_cancer_data.csv")
df = pd.read_csv(r"C:\Users\liam\Pictures\apple its glowtime\iPhone 16\dataset_med.csv")

# Drop irrelevant columns
df = df.drop(columns=["id", "diagnosis_date", "end_treatment_date"], errors="ignore")

# Map cancer_stage to numeric
df["cancer_stage"] = df["cancer_stage"].map(
    {"Stage I": 1, "Stage II": 2, "Stage III": 3, "Stage IV": 4}
)

# Split survivors and non-survivors
survivors, non_survivors = df[df["survived"] == 1], df[df["survived"] == 0]

# Initialize table
comparison = []

# Categorical comparison
categorical_cols = [
    "gender",
    "country",
    "family_history",
    "smoking_status",
    "hypertension",
    "asthma",
    "cirrhosis",
    "other_cancer",
    "treatment_type",
]

for col in categorical_cols:
    if col in df.columns:
        surv_common = survivors[col].mode()[0]
        surv_count = survivors[col].value_counts().iloc[0]
        dead_common = non_survivors[col].mode()[0]
        dead_count = non_survivors[col].value_counts().iloc[0]
        comparison.append(
            [col, f"{surv_common} ({surv_count})", f"{dead_common} ({dead_count})"]
        )

# Numeric comparison
numeric_cols = ["age", "bmi", "cholesterol_level", "cancer_stage"]

for col in numeric_cols:
    if col in df.columns:
        surv_mean = survivors[col].mean()
        dead_mean = non_survivors[col].mean()
        comparison.append([col, f"{surv_mean:.2f}", f"{dead_mean:.2f}"])

# Create DataFrame
comparison_df = pd.DataFrame(
    comparison, columns=["Trait", "Survivors", "Non-Survivors"]
)

# Display the table
print("\n📋 Trait Comparison Table:\n")
print(comparison_df.to_string(index=False))
