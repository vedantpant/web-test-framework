from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    def handle_route(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body='["FAKE_COMPANY_1", "FAKE_COMPANY_2"]'
        )


    page.route("**/data/company_logos.json", handle_route)

    page.goto("https://reqres.in/")
    page.wait_for_timeout(3000)

    browser.close()