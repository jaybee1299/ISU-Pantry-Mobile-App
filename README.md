# ISU School Pantry Mobile Signup & AI Assistant

## Project Overview

This project focuses on developing a mobile application for the ISU School Pantry. The application will allow pantry users and volunteers to create accounts and complete the signup process through their phones. The application will also include an AI assistant that can answer common questions about registration, pantry services, and volunteer opportunities using information collected from verified pantry sources.


## Data Sources

The initial dataset contains information related to the School Street Food Pantry, including general pantry information, eligibility, services, location, and volunteer opportunities. The information was collected from official Illinois State University sources and organized into a FAQ-style dataset that can later be used by the application's AI assistant.

The raw dataset is stored in `data/pantry_faq_raw.csv`.

## Dataset Size

The initial dataset contains 10 records and 6 columns:

- `id` - unique identifier for each record
- `category` - type of pantry information
- `audience` - identifies whether the information is for pantry users, volunteers, or both
- `question` - common question a user may ask
- `answer` - verified answer to the question
- `source` - source of the information

- ## Data Cleaning

The dataset was cleaned using a Python script located at `scripts/clean_data.py`. The script reads the raw CSV file and performs several cleaning steps:

- Removes extra whitespace from the data.
- Standardizes the `category` and `audience` fields to lowercase.
- Removes records that are missing a question, answer, or source.
- Checks for and removes duplicate questions.
- Saves the cleaned results as `data/pantry_faq_clean.csv`.

The raw dataset contained 10 records. After running the cleaning process, 10 records remained, meaning no records needed to be removed from the initial dataset.

## Envisioned Workflow

```mermaid
flowchart TD
    A[Mobile App] --> B{Choose User Type}
    B --> C[Pantry User]
    B --> D[Volunteer]
    C --> E[Registration / Signup]
    D --> E
    E --> F[Account Created]
    F --> G[AI Assistant]
    G --> H[User Asks a Question]
    H --> I[Search Clean Pantry FAQ Data]
    I --> J[Retrieve Relevant Information]
    J --> K[AI Generates Response]
    K --> L[Response Displayed in Mobile App]
## Next Steps

The next phase of the project will focus on designing and developing the mobile application. This will include creating the pantry user and volunteer registration interfaces, storing account information, and connecting the cleaned pantry dataset to the AI assistant. The dataset will also be expanded as additional verified information becomes available.
```
