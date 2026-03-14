import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        context.tracing.start(name="test_code", screenshots=True, snapshots=True)

        page = context.new_page()
        yield page

        context.tracing.stop(path="./test-results/trace.zip")  # ← Creates HERE
        browser.close()
