import time
import json
from playwright.sync_api import expect

def test_slow_connection_eventually_connect(page):
    def handle_route(route):
        print(f"\n[{time.time():.2f}] Mock handler started")
        page.wait_for_timeout(4000)
        print(f"[{time.time():.2f}] About to fulfill")
        fake_data = [{"companyName": "ConnectedDevice", "link": "https://example.com", "logo": "/img/logos/device.png", "dark": False, "weight": "standard"}]
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(fake_data)
        )
        print(f"[{time.time():.2f}] Fulfilled")

    page.route("**/data/company_logos.json", handle_route)

    start = time.time()
    page.goto("https://reqres.in")
    elapsed_time = time.time() - start

    logo_link = page.locator(".rr-logo").filter(has_not=page.locator(".rr-logo__cta-text"))
    expect(logo_link).to_have_count(1, timeout=10000)
    print(f"\nConnection took {elapsed_time:.2f}s but succeeded")