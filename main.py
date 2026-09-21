from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from redaction import redact_sensitive_data


app = FastAPI()

templates = Jinja2Templates(directory="templates")

messages = []
next_id = 1


class MessageRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "SDET Home Challenge is running!"
    }


@app.post("/messages")
def create_message(request: MessageRequest):
    global next_id

    redacted_message = redact_sensitive_data(request.message)

    message = {
        "id": next_id,
        "message": redacted_message
    }

    messages.append(message)
    next_id += 1

    return {
        "message": "Message received successfully",
        "data": message
    }


@app.get("/messages")
def get_messages():
    return {
        "messages": messages
    }


@app.delete("/messages/{message_id}")
def delete_message(message_id: int):
    global next_id

    for message in messages:
        if message["id"] == message_id:
            messages.remove(message)

            # Renumber remaining messages
            for index, message in enumerate(messages, start=1):
                message["id"] = index

            next_id = len(messages) + 1

            return {
                "message": "Message deleted successfully"
            }

    return {
        "message": "Message not found"
    }


@app.get("/web", response_class=HTMLResponse)
def web_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "messages": messages
        }
    )
