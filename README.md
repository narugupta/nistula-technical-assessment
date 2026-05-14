# Nistula AI Hospitality Platform

A production-oriented guest messaging and AI orchestration platform built for the Nistula Technical Assessment (Role A — Backend & Intelligence).

The system receives guest messages from multiple hospitality channels, normalises them into a unified schema, generates AI-drafted replies using Claude, scores confidence, and routes each message into the correct operational workflow:

* auto_send
* agent_review
* escalate

The project was designed not just as a chatbot backend, but as an operational reliability layer for hospitality workflows.

---

# Features

* Multi-channel inbound guest messaging
* Unified message normalisation
* Query classification
* Claude AI reply generation
* Confidence scoring engine
* Automated workflow routing
* Escalation management
* SLA tracking
* Conversation threading
* Guest memory/context injection
* Replay attack protection
* Operational metrics
* Dead letter queue for failed workflows
* PostgreSQL persistence
* Minimal frontend dashboard for evaluator testing
* Dockerized deployment

---

# Tech Stack

## Backend

* Python 3.11
* FastAPI
* SQLAlchemy Async ORM
* PostgreSQL
* Anthropic Claude API
* Pydantic
* Uvicorn

## Frontend

* React
* Vite

## Infrastructure

* Docker
* Docker Compose

---

# Why Docker Was Used

Docker was used to ensure:

* consistent local environments
* predictable PostgreSQL networking
* evaluator-friendly setup
* simpler dependency management
* deployment portability

This avoids common issues involving:

* PostgreSQL installation
* asyncpg compatibility
* Python version mismatches
* environment configuration inconsistencies

The backend and database run inside isolated containers, closely matching a real production deployment workflow.

---

# Architecture Overview

```text
Inbound Message
      │
      ▼
Replay Protection
      │
      ▼
Message Normalisation
      │
      ▼
Query Classification
      │
      ▼
Claude AI Reply Generation
      │
      ▼
Confidence Scoring
      │
      ▼
Action Routing
(auto_send / agent_review / escalate)
      │
      ▼
Background Persistence
      │
      ├── Conversation Threading
      ├── Escalation Creation
      ├── Metrics Logging
      ├── Event Logging
      └── Dead Letter Capture
```

---

# Project Structure

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── middleware/
│   ├── models/
│   ├── prompts/
│   ├── services/
│   └── utils/
│
├── tests/
├── requirements.txt
├── schema.sql
└── README.md

frontend/
├── src/
├── public/
├── package.json
└── vite.config.js
```

---

# Quick Start

## 1. Clone the Repository

```bash
git clone https://github.com/narugupta/nistula-technical-assessment
cd nistula-technical-assessment
```

---

# Running with Docker (Recommended)

## Start Backend + Database

From the project root:

```bash
docker compose up --build
```

This starts:

* FastAPI backend
* PostgreSQL database

Backend API:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

## Start Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

The frontend allows evaluators to:

* send guest messages
* view AI-generated replies
* test escalation routing
* inspect operational metrics
* verify full workflow orchestration visually

The frontend was intentionally kept lightweight because the assessment focus is backend orchestration and systems design.

---

# Local Development Setup (Without Docker)

## Backend Setup

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn app.main:app --reload --port 8000
```

---

# Environment Variables

Create a `.env` file inside `backend/`

```env
ANTHROPIC_API_KEY=your_api_key_here

DATABASE_URL=postgresql+asyncpg://nistula:nistula_password@localhost:5432/nistula_db
```

---

# Local vs Docker Database Configuration

## Local Development

```env
DATABASE_URL=postgresql+asyncpg://nistula:nistula_password@localhost:5432/nistula_db
```

## Docker Compose

```env
DATABASE_URL=postgresql+asyncpg://nistula:nistula_password@db:5432/nistula_db
```

Why:

* `localhost` works outside Docker
* `db` only resolves inside Docker networking

Docker Compose overrides the environment automatically for container-to-container communication.

---

# API Endpoints

## POST `/webhook/message`

Receives a guest message, generates an AI reply, scores confidence, and routes the workflow.

### Supported Channels

* whatsapp
* booking_com
* airbnb
* instagram
* direct

### Example Payload

```json
{
  "source": "whatsapp",
  "guest_name": "Rahul Sharma",
  "message": "Is the villa available from April 20 to 24?",
  "timestamp": "2026-05-05T10:30:00Z",
  "booking_ref": "NIS-2024-0891",
  "property_id": "villa-b1"
}
```

---

## GET `/operations/escalations`

Returns escalation records with:

* severity
* assigned agent
* SLA deadline
* status

---

## GET `/operations/metrics`

Returns operational metrics:

* total messages
* escalations
* failed events
* auto-send counts

---

## GET `/health`

Basic health check endpoint.

---

# Confidence Scoring Logic

The confidence score determines whether the AI reply is:

* auto-sent
* routed for review
* escalated to humans

The scoring starts from a baseline value and adjusts dynamically based on:

* message clarity
* operational risk
* query type
* AI certainty

| Signal                              | Adjustment |
| ----------------------------------- | ---------- |
| Clear booking context               | +0.15      |
| Non-complaint query                 | +0.15      |
| Detailed message                    | +0.10      |
| Direct operational answer           | +0.10      |
| Vague or ambiguous message          | -0.20      |
| Complaint or refund-related message | -0.30      |
| AI uncertainty detected             | -0.15      |

## Final Action Thresholds

| Score       | Action       |
| ----------- | ------------ |
| > 0.85      | auto_send    |
| 0.60 – 0.85 | agent_review |
| < 0.60      | escalate     |

The scoring system is intentionally conservative for complaints and operationally risky situations.

---

# Query Classification

Messages are classified into:

* pre_sales_availability
* pre_sales_pricing
* post_sales_checkin
* special_request
* complaint
* general_enquiry

Classification currently uses lightweight keyword-based routing for explainability and simplicity.

Production systems would likely evolve toward ML/NLP classification models.

---

# Database Design

The PostgreSQL schema supports:

* unified guest profiles
* multi-channel messaging
* reusable conversation threads
* escalation workflows
* AI metadata tracking
* SLA monitoring
* operational observability

Key tables:

* guests
* channel_identities
* guest_profiles
* reservations
* conversations
* messages
* escalations
* message_events
* processing_metrics
* failed_events

Full schema:

```text
schema.sql
```

---

# Frontend Demo UI

A lightweight frontend dashboard was added so evaluators can test the platform end-to-end without needing Postman or manual database inspection.

The frontend supports:

* sending guest messages
* viewing AI replies
* viewing escalations
* viewing operational metrics

---

# End-to-End Testing

## 1. Start Docker Services

```bash
docker compose up --build
```

## 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

## 3. Open Frontend

```text
http://localhost:5173
```

## 4. Send Guest Messages

Test:

* availability enquiries
* pricing questions
* complaints
* check-in requests

## 5. Verify Database

```bash
docker exec -it nistula_db psql -U nistula -d nistula_db
```

Example queries:

```sql
SELECT * FROM messages;

SELECT * FROM escalations;

SELECT * FROM processing_metrics;
```

---

# Problems Faced During Development

## 1. Pytest Could Not Import `app`

### Error

```text
ModuleNotFoundError: No module named 'app'
```

### Fix

Added:

```ini
[pytest]
pythonpath = .
```

inside:

```text
pytest.ini
```

---

## 2. Anthropic Dependency Worked in Docker but Failed Locally

### Error

```text
ModuleNotFoundError: No module named 'anthropic'
```

### Cause

The dependency existed inside Docker but was not installed locally.

### Fix

```bash
python -m pip install -r requirements.txt
```

---

## 3. Docker vs Local PostgreSQL Hostname

### Problem

`db` only resolves inside Docker networking.

### Correct Fix

Local:

```env
localhost
```

Docker:

```env
db
```

Docker Compose overrides the variable automatically.

---

# Known Limitations

* Replay protection currently uses in-memory caching
* Rate limiting is in-memory only
* Guest identity resolution is still naive
* Query classification is keyword-based
* Redis is not yet integrated
* No PMS integration yet
* No vector memory/search yet

These were intentionally kept lightweight for the assessment scope.

---

# Future Improvements

* Redis-backed replay protection
* ML/NLP classification
* Vector memory retrieval
* PMS integration
* Multi-property management
* Real WhatsApp/Twilio integration
* Human agent dashboard
* Retry queues and worker orchestration
* Kubernetes deployment
* Observability stack (Prometheus + Grafana)

---

# Design Philosophy

The goal of this project was not only generating AI replies.

The system was designed as an operational orchestration platform focused on:

* reliability
* escalation safety
* observability
* workflow accountability
* hospitality operations
* future scalability

The emphasis was building the surrounding operational layer required to safely use AI in real guest communication workflows.
