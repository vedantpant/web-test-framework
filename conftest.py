import pytest
import os
from playwright.sync_api import sync_playwright
from datetime import datetime

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser =p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    """Hook: Save screenshot if playwright test fails."""
    if "page" not in request.fixturenames:
        yield
        return

    page = request.getfixturevalue('page')
    yield
    if request.node.rep_call.failed:

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/failure_{request.node.name}_{timestamp}.png"
        os.makedirs("screenshots", exist_ok=True)
        page.screenshot(path=screenshot_path)
        print(f"\n[Screenshot] saved to: {screenshot_path}")