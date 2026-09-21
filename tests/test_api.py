from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_email_is_redacted():
    response = client.post(
        "/messages",
        json={"message": "My email is test@gmail.com"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["message"] == "My email is *est@gmail.com"


def test_ip_is_redacted():
    response = client.post(
        "/messages",
        json={"message": "My IP is 192.168.1.10"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["message"] == "My IP is X.X.X.10"


def test_credit_card_is_redacted():
    response = client.post(
        "/messages",
        json={"message": "My card is 1234 5678 9012 1111"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["message"] == "My card is XXXXXXXXXXXX1111"


def test_jwt_is_redacted():
    token = (
        "eyJhbGciOiJIUzI1NiJ9."
        "eyJzdWIiOiIxMjMifQ."
        "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    )

    response = client.post(
        "/messages",
        json={"message": f"My token is {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["message"] == "My token is JWT"


def test_get_messages():
    response = client.get("/messages")

    assert response.status_code == 200

    data = response.json()

    assert "messages" in data


def test_delete_message():
    response = client.post(
        "/messages",
        json={"message": "Message to delete"}
    )

    message_id = response.json()["data"]["id"]

    delete_response = client.delete(
        f"/messages/{message_id}"
    )

    assert delete_response.status_code == 200

    assert delete_response.json()["message"] == (
        "Message deleted successfully"
    )