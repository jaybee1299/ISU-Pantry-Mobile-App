import csv
import os

# File locations
input_file = "data/pantry_faq_raw.csv"
output_file = "data/pantry_faq_clean.csv"

# Read the raw data
with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

print("Raw records:", len(rows))

cleaned_rows = []
seen_questions = set()

for row in rows:

    # Remove extra spaces
    for column in row:
        if row[column]:
            row[column] = row[column].strip()

    # Standardize category and audience
    row["category"] = row["category"].lower()
    row["audience"] = row["audience"].lower()

    # Skip rows with missing important information
    if not row["question"] or not row["answer"] or not row["source"]:
        continue

    # Remove duplicate questions
    question = row["question"].lower()

    if question in seen_questions:
        continue

    seen_questions.add(question)
    cleaned_rows.append(row)

# Create the cleaned CSV
with open(output_file, "w", newline="", encoding="utf-8") as file:
    fieldnames = ["id", "category", "audience", "question", "answer", "source"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(cleaned_rows)

print("Clean records:", len(cleaned_rows))
print("Cleaned file created:", output_file)
