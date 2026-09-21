import json

def test_handle_fake_companies(page):
    fake_companies = [
        {"companyName": "FakeCorp1", "link": "https://fake1.com", "logo": "/img/logos/fake1.png", "dark": False, "weight": "standard"},
        {"companyName": "FakeCorp2", "link": "https://fake2.com", "logo": "/img/logos/fake2.png", "dark": False, "weight": "standard"},
        {"companyName": "FakeCorp3", "link": "https://fake3.com", "logo": "/img/logos/fake3.png", "dark": False, "weight": "standard"},
                
    ]
    def handle_route(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(fake_companies)
        )

    page.route("**/data/company_logos.json", handle_route)

    page.goto("https://reqres.in/")

    page.wait_for_load_state("networkidle")

    logo_link = page.locator(".rr-logo").filter(has_not=page.locator(".rr-logo__cta-text"))

    assert logo_link.count() == 3