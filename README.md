# Enterprise CRUD Dashboard Suite

**Author:** Jatin

A full-stack Python application designed to demonstrate **end-to-end system design**, including **backend APIs**, **database modeling**, **CRUD workflows**, and a **business dashboard UI**.

---

## Overview

This project simulates a real-world **business operations dashboard** where users can manage entities like **Projects, Customers, Tasks, Risks, Invoices, and Milestones**.

It focuses on:
- **Clean Architecture**
- **Scalability**
- **Maintainability**

---

## Features

- Professional **Dashboard UI** with multiple modules  
- Complete **CRUD Operations** across all entities  
- **SQLite Database** with structured schema  
- **Audit Logging** (create, update, delete tracking)  
- **Search Functionality** across records  
- **Canvas-based Analytics Charts**  
- **CSV Export APIs**  
- Premium UI with **animated background**  
- No external dependencies (**pure Python**)  

---

## Tech Stack

- **Backend:** Python  
- **Database:** SQLite  
- **Frontend:** HTML, CSS, JavaScript  
- **Architecture:** Modular (Routes, Services, Core)  

---

## Project Structure


app/
├── core/ # Configuration, database setup, response handling
├── routes/ # API endpoints
├── services/ # Business logic layer
├── templates/ # HTML UI files
├── static/ # CSS, JavaScript assets
└── main.py # Application entry point

scripts/
└── reset_database.py # Database reset utility

tests/
└── test_smoke.py # Basic smoke tests


---

## Getting Started

### Run the Application

```bash
python -m app.main

or

py -m app.main
Database Reset (Optional)
python scripts/reset_database.py
Testing
pytest
Key Highlights
Demonstrates full-stack ownership (UI + Backend + Database)
Implements real-world business workflows
Follows separation of concerns
Includes analytics, logging, and export features
Structured for scalability and maintainability
Future Enhancements
Add Authentication & Role-Based Access Control
Integrate Swagger API Documentation
Migrate to PostgreSQL / Cloud Database
Add Docker & CI/CD pipeline
License

This project is intended for educational and interview purposes.
