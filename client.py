import argparse
import requests

BASE_URL = "http://127.0.0.1:8000"


def send_message(message):
    response = requests.post(
        f"{BASE_URL}/messages",
        json={"message": message}
    )
    response.raise_for_status()
    return response.json()


def get_messages():
    response = requests.get(
        f"{BASE_URL}/messages"
    )
    response.raise_for_status()
    return response.json()


def delete_message(message_id):
    response = requests.delete(
        f"{BASE_URL}/messages/{message_id}"
    )
    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="SDET Message Client"
    )

    parser.add_argument(
        "action",
        choices=["post", "get", "delete"],
        help="Choose post, get, or delete"
    )

    parser.add_argument(
        "--message",
        help="Message to send"
    )

    parser.add_argument(
        "--id",
        type=int,
        help="Message ID to delete"
    )

    args = parser.parse_args()

    if args.action == "post":
        if not args.message:
            parser.error("--message is required when using post")

        result = send_message(args.message)
        print(result)

    elif args.action == "get":
        result = get_messages()
        print(result)

    elif args.action == "delete":
        if args.id is None:
            parser.error("--id is required when using delete")

        result = delete_message(args.id)
        print(result)


if __name__ == "__main__":
    main()