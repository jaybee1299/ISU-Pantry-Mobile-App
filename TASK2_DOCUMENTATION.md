# Task 2 – Second Working Prototype
**Project:** ISU School Pantry Mobile Signup & AI Assistant  
**Course:** 244 Projects  
**Due Date:** October 6, 2026

## 1. Second Working Prototype

The second prototype expands the original AI pantry assistant by adding a web-based signup system for pantry users and volunteers. The application is developed using Python, Flask, HTML, CSS, and JavaScript.

Users can select their signup role, enter their name, email, phone number, and availability or additional notes, and submit the form. The application processes the submission, saves the information in a SQLite database, and displays a confirmation message.

The AI assistant remains available to answer questions about pantry services, eligibility, registration, location, and volunteer opportunities. It uses Sentence Transformers and ChromaDB to retrieve relevant answers from the cleaned pantry FAQ dataset.

The prototype was tested by submitting a pantry user registration, verifying the success message, and checking that the registration was stored in SQLite. The AI assistant was also tested through the web interface.

## 2. Design Alternatives

Flask was selected because it is lightweight, works well with Python, and supports the current prototype without requiring a complex framework. Django is an alternative for a larger application with built-in administrative and authentication features.

SQLite was selected for signup storage because it is simple, requires no separate database server, and supports persistent records. PostgreSQL or MySQL would be more appropriate for a production application with many concurrent users.

ChromaDB was selected for the AI assistant because it supports vector similarity searches and integrates with Sentence Transformers.

## 3. Scalability

The current prototype is designed for demonstration and small-scale testing. As usage increases, the application could be deployed on a cloud server, and the signup database could be migrated to PostgreSQL.

Additional improvements could include user authentication, administrator access, form validation, database backups, and more comprehensive testing.

The AI assistant could also be expanded with additional verified pantry information and a larger vector database.

## 4. Data Design and Persistence

The application uses two main types of data:

- **Reference data:** Cleaned pantry FAQ records stored in a CSV file and converted into vector embeddings for retrieval through ChromaDB.
- **Operational data:** Pantry user and volunteer signup information stored in SQLite.

The signup database stores registration details, including the user's selected role, name, email, phone number, availability or notes, and submission timestamp.

SQLite provides persistence so registration records remain available after the application stops and restarts. ChromaDB stores the vectorized FAQ information for reuse by the AI assistant.

The local SQLite database is excluded from GitHub to avoid publishing personal registration information.

## 5. GitHub Repository

The repository contains the Flask application, web interface, cleaned FAQ dataset, preprocessing scripts, vector database, dependencies, and project documentation.

**Repository:** https://github.com/jaybee1299/ISU-Pantry-Mobile-App

The second prototype adds signup functionality and SQLite persistence while retaining the original AI assistant.
