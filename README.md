
# Multi-Format Intake Agent with Intelligent Routing & Context Memory

## 🔍 Objective

Build a multi-agent AI system that can intelligently process and classify inputs in **PDF**, **JSON**, or **Email (text)** formats. Based on the format and intent, the input is routed to a specialized agent for extraction. The system maintains a lightweight context memory to support downstream chaining or audit trails.

---

## 🧠 System Overview

### 1. Classifier Agent
- Receives raw input (text, JSON, or PDF file)
- Determines:
  - **Format**: PDF / JSON / Email
  - **Intent**: Invoice, RFQ, Complaint, Regulation, etc.
- Routes input to the appropriate agent
- Stores format + intent metadata in shared memory

### 2. JSON Agent
- Accepts structured JSON data (e.g., API/webhook payloads)
- Extracts and formats data into a predefined schema (e.g., FlowBit format)
- Detects anomalies or missing fields

### 3. Email Parser Agent
- Accepts plain or HTML email body text
- Extracts sender, urgency, and request intent
- Stores conversation ID + metadata in shared memory

### 4. Shared Memory
- Stores:
  - Input metadata (type, source, timestamp)
  - Extracted fields by agent
  - Thread/conversation ID (if any)
- Implemented using in-memory Python class (can be upgraded to Redis or SQLite)

---

## 🔄 End-to-End Flow Example

1. User submits an email body.
2. Classifier determines format = `email`, intent = `RFQ`.
3. Routed to Email Agent → extracts sender, intent, urgency.
4. Memory logs result.
5. If RFQ contains embedded JSON → routed to JSON Agent too.
6. Combined structured output returned.

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **FastAPI** – API framework
- **Uvicorn** – ASGI server
- **Postman** – for manual API testing
- **Docker** – optional containerization

---

## 🚀 Usage

### Run Locally

```bash
git clone https://github.com/your-username/multi-format-intake-agent.git
cd multi-format-intake-agent
pip install -r requirements.txt
uvicorn main:app --reload
```

### API Endpoints

#### 1. POST `/intake/`

Classifies and routes input.

**Body Formats Supported**:
- `application/json` → JSON agent
- `text/plain` → Email agent
- `application/pdf` → (Not implemented)

#### 2. GET `/memory/`
Returns all stored memory (metadata and fields).

---

## 📂 Project Structure

```
multi-format-intake-agent/
├── main.py                  # FastAPI app & classifier routing
├── agents/
│   ├── classifier_agent.py
│   ├── email_agent.py
│   └── json_agent.py
├── memory/
│   ├── memory.py
│   └── redis_memory.py      # (optional for upgrade)
├── utils/
│   ├── schema.py
│   ├── pdf_utils.py
│   └── email_utils.py
├── tests/                   # Pytest unit tests
└── requirements.txt
```

---

## 🧪 Testing

Run all tests using:

```bash
pytest tests/
```

---

## 🐳 Docker (Optional)

To run in Docker:

```bash
docker build -t intake-agent .
docker run -p 8000:8000 intake-agent
```

---

## 📌 Notes

- PDF routing is stubbed; placeholder message is returned.
- Memory implementation is extensible.

---

## 👤 Author

Developed by [Your Name or GitHub](https://github.com/your-username)
