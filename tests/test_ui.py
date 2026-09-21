from playwright.sync_api import sync_playwright
import uuid


def test_webpage_message_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page()

        page.goto("http://127.0.0.1:8000/web")

        unique_id = uuid.uuid4().hex

        marker = f"PLAYWRIGHT_TEST_{unique_id}"

        email = f"test_{unique_id}@example.com"

        message = (
            f"{marker} - My email is {email}"
        )

        page.locator("#messageInput").fill(message)

        page.get_by_role(
            "button",
            name="Send"
        ).click()

        page.wait_for_load_state("networkidle")

        message_row = page.locator("tr").filter(
            has_text=marker
        )

        assert message_row.count() == 1

        row_text = message_row.inner_text()

        expected_email = (
            "*" * (len(f"test_{unique_id}") - 3)
            + f"test_{unique_id}"[-3:]
            + "@example.com"
        )

        assert expected_email in row_text

        assert email not in row_text

        delete_button = message_row.get_by_role(
            "button",
            name="Delete"
        )

        assert delete_button.count() == 1

        with page.expect_response(
            lambda response:
                response.request.method == "DELETE"
                and "/messages/" in response.url
        ) as response_info:

            delete_button.click()

        delete_response = response_info.value

        assert delete_response.status == 200

        page.wait_for_load_state("networkidle")

        message_row = page.locator("tr").filter(
            has_text=marker
        )

        assert message_row.count() == 0

        browser.close()