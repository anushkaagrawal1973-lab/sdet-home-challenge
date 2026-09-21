# SDET Home Challenge

A simple Python-based message API with sensitive-data redaction, a web interface, a CLI client, automated API tests, and Playwright UI tests.

## Features

* REST API for creating and retrieving messages
* Sensitive data redaction before storage:

  * Email addresses
  * IPv4 addresses
  * JWT tokens
  * Credit card numbers
* Basic web interface for viewing messages
* Delete message operation
* Python CLI client
* Automated API tests using pytest
* UI automation using Playwright
* Docker support

## Project Structure

```text
sdet-home-challenge/
├── main.py
├── redaction.py
├── client.py
├── requirements.txt
├── Dockerfile
├── README.md
├── templates/
│   └── index.html
└── tests/
    ├── test_api.py
    └── test_ui.py
```

## Requirements

* Python 3.11+
* Docker Desktop
* Playwright

## Run Locally

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the Playwright browser:

```bash
python -m playwright install
```

Start the application:

```bash
python -m uvicorn main:app --reload
```

Open the web interface:

```text
http://127.0.0.1:8000/web
```

## API Endpoints

### Create a message

```http
POST /messages
```

Example request:

```json
{
  "message": "My email is test@gmail.com"
}
```

Sensitive information is redacted before the message is stored.

### Get messages

```http
GET /messages
```

### Delete a message

```http
DELETE /messages/{message_id}
```

## Redaction Examples

| Sensitive data | Example               | Redacted           |
| -------------- | --------------------- | ------------------ |
| Email          | `test@gmail.com`      | `*est@gmail.com`   |
| IPv4           | `192.168.1.10`        | `X.X.X.10`         |
| JWT            | JWT token             | `JWT`              |
| Credit card    | `1234 5678 9012 1111` | `XXXXXXXXXXXX1111` |

## CLI Client

Send a message:

```bash
python client.py post --message "My email is test@gmail.com"
```

Retrieve messages:

```bash
python client.py get
```

Delete a message:

```bash
python client.py delete --id 1
```

## Running Tests

Run all tests:

```bash
python -m pytest -q
```

Run API tests:

```bash
python -m pytest tests/test_api.py -q
```

Run Playwright UI tests:

```bash
python -m pytest tests/test_ui.py -q
```

The Playwright test requires the application to be running.

## Docker

Build the Docker image:

```bash
docker build -t sdet-home-challenge .
```

Run the container:

```bash
docker run -p 8000:8000 sdet-home-challenge
```

Then open:

```text
http://127.0.0.1:8000/web
```

## Testing Approach

The API tests verify:

* Message creation
* Email redaction
* IPv4 redaction
* JWT redaction
* Credit card redaction
* Message retrieval
* Message deletion

The Playwright test verifies the web application flow by:

1. Opening the web page
2. Entering a message containing an email address
3. Submitting the message
4. Verifying that the email is redacted on the page
5. Verifying that the original email is not displayed
6. Deleting the message
7. Verifying that the message is removed from the page

## Difficulties Faced

One of the main challenges was creating regular expressions that could correctly identify different types of sensitive information while avoiding changes to normal text.

Another challenge was making sure the redaction happened before the data was stored, so the original sensitive information was not available in the stored message.

For the UI testing, I had to make sure Playwright could find the correct message and verify that the redacted value was displayed instead of the original sensitive data.

I also had to handle the Docker setup and make sure the application and its dependencies worked correctly inside the container.

## Room for Improvement

Possible future improvements include:

* Persistent database storage
* Authentication and authorization
* Better input validation
* More comprehensive redaction rules
* Improved UI and user feedback
