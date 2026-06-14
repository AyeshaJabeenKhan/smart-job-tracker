# Smart Job Tracker

Smart Job Tracker is an automated, AI-driven backend application designed to streamline the job hunt ecosystem. Instead of relying on manual data entry, the application leverages an advanced AI extraction architecture to isolate core parameters from raw, unformatted job descriptions and instantly maps them to a structured database schema. 

The system also includes an automated intelligence preparation engine that generates highly targeted technical interview questions tailored to the specific company requirements and engineering stack extracted from the post.

## System Architecture & Features

### 1. AI Data Extraction Engine
* **Asynchronous Text Parsing:** Processes raw text fragments pasted directly from platforms like LinkedIn, Indeed, or internal career portals.
* **Structured Data Mapping:** Uses Google Gemini (via the official Google GenAI SDK) to parse unstructured layouts. The data is strictly validated against Pydantic models before ingestion.
* **Automated Parameter Isolation:** Isolates targeted parameters such as Corporate Entity (Company Name), Target Job Title, and Job Board Origin URLs.

### 2. Automated Intelligence Prep Module
* **Tailored Question Generation:** Evaluates company tech stacks and role requirements to generate high-fidelity interview questions.
* **Context-Driven Evaluation:** Provides explicit hints focused on demonstrating deep architectural understanding, performance tradeoffs, and system strengths.

### 3. Core Relational Database Pipeline
* **SQLAlchemy ORM Layer:** Maps data directly into operational database schemas.
* **Pagination & Performance Filtering:** Embedded database-level pagination (`skip` and `limit` controls) ensures low latency when dealing with large collections of tracked application records.
* **Full CRUD Operational Flow:** Exposes structured FastAPI endpoints for Instantiation, Collection Fetching, Individual Resource Retrieval, In-place Mutation, and Secure Deletion.

## Tech Stack

* **Backend Engine:** Python, FastAPI
* **AI Core:** Google GenAI SDK (Gemini 2.5 Flash)
* **Data Layer:** SQLAlchemy ORM, Pydantic v2 (Data Validation & Serialization)
* **Architecture Style:** RESTful API with structured routing structures

## Local Installation & Environment Setup

### Prerequisites
* Python 3.11 or higher
* A Google AI Studio account and Gemini API Key

### Installation

1. Clone the repository to your workspace:
   ```bash
   git clone [https://github.com/AyeshaJabeenKhan/smart-job-tracker.git](https://github.com/AyeshaJabeenKhan/smart-job-tracker.git)
   cd smart-job-tracker

    Install dependency architectures:
    Bash

    pip install fastapi uvicorn google-genai sqlalchemy pydantic python-dotenv

    Configure Environment Variables:
    Create a .env file in the root directory of the project to securely house structural targets:
    Code snippet

    GEMINI_API_KEY="your_actual_api_key_here"

    Launch the application server:
    Bash

    uvicorn app.main:app --reload --port 8001

    The local API interface and dashboard will be accessible at http://127.0.0.1:8001.

API Documentation Reference

The interface exposes standard endpoints organized by functional domain:

Method,Endpoint,Description

POST,/api/v1/jobs/,Instantiates a new tracking record inside the persistent engine.
GET,/api/v1/jobs/,Fetches a paginated collection of tracked applications.
GET,/api/v1/jobs/{id},Retrieves a single application record by its unique Primary Key.
PUT,/api/v1/jobs/{id},Mutates existing fields on a tracking asset based on delta updates.
DELETE,/api/v1/jobs/{id},Safely expunges a job application from local storage.
POST,/api/v1/jobs/parse-ai,Feeds raw text to the Gemini model to parse into structured schemas.
