# main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from agents.text_agent import TextAgent
from memory.memory import Memory
# If using Redis instead:
# from memory.redis_memory import RedisMemory
import uvicorn

app = FastAPI(title="Multi-Format Intake Agent")

# Initialize memory and agents
shared_memory = Memory()  # Or RedisMemory()
classifier = ClassifierAgent(memory=shared_memory)
json_agent = JSONAgent(memory=shared_memory)
email_agent = EmailAgent(memory=shared_memory)
text_agent = TextAgent(memory=shared_memory)

@app.get("/")
async def root():
    """
    Root endpoint to confirm service is running.
    """
    return {
        "message": "✅ Multi-Format Intake Agent is running.",
        "docs_url": "/docs",
        "status": "running"
    }

@app.post("/intake/")
async def intake_endpoint(request: Request):
    """
    Accepts raw input (JSON, Email, Text, or PDF), classifies it,
    and routes to appropriate agent for structured extraction.
    """
    content_type = request.headers.get("Content-Type", "")
    body = await request.body()

    # Decode text input
    try:
        text_input = body.decode("utf-8")
    except Exception:
        text_input = body

    # Collect metadata (for logging/classification)
    metadata = {
        "source": request.client.host,
        "timestamp": request.headers.get("X-Timestamp")  # Optional
    }

    # Step 1: Classify input format and intent
    input_format, intent = classifier.classify(text_input, metadata)

    response = {
        "format": input_format,
        "intent": intent,
        "output": {}
    }

    # Step 2: Route to appropriate agent
    if input_format == "json":
        output = json_agent.handle_json(text_input)
        response["output"]["json"] = output

    elif input_format == "email":
        output = email_agent.handle_email(text_input)
        response["output"]["email"] = output

        # Optional: Parse embedded JSON if present in RFQ-type emails
        if intent == "rfq" and "{" in text_input:
            output_json = json_agent.handle_json(text_input)
            response["output"]["json_extracted"] = output_json

    elif input_format == "pdf":
        response["output"]["message"] = "PDF routing not yet implemented"

    elif input_format == "text":
        output = text_agent.handle_text(text_input)
        response["output"]["text"] = output

    else:
        response["output"]["error"] = "Unsupported or unknown format"

    return JSONResponse(content=response)

@app.get("/memory/")
def view_memory():
    """
    Retrieve in-memory storage for inspection/testing.
    """
    return {
        "metadata": shared_memory.get_all_metadata(),
        "fields": {
            "json_agent": shared_memory.get_agent_fields("json_agent"),
            "email_agent": shared_memory.get_agent_fields("email_agent"),
            "text_agent": shared_memory.get_agent_fields("text_agent"),
        }
    }

@app.post("/memory/clear/")
def clear_memory():
    """
    Clear all memory.
    """
    shared_memory.clear()
    return {"status": "Memory cleared."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
