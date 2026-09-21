import re


def mask_email(match):
    email = match.group(0)
    username, domain = email.split("@")

    if len(username) <= 3:
        masked = "*" * len(username)
    else:
        masked = "*" * (len(username) - 3) + username[-3:]

    return masked + "@" + domain


def mask_ip(match):
    ip = match.group(0)
    last_part = ip.split(".")[-1]

    return "X.X.X." + last_part


def mask_credit_card(match):
    card = re.sub(r"[- ]", "", match.group(0))

    return "X" * (len(card) - 4) + card[-4:]


def redact_sensitive_data(text):

    # Email
    text = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        mask_email,
        text
    )

    # IPv4
    text = re.sub(
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        mask_ip,
        text
    )

    # JWT
    text = re.sub(
        r'\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b',
        'JWT',
        text
    )

    # Credit card
    text = re.sub(
        r'\b(?:\d{4}[- ]?){3}\d{4}\b',
        mask_credit_card,
        text
    )

    return text