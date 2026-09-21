def test_handles_broken_company_logos_response(page):
    def handle_route(route):
            route.fulfill(
                status=500,
                content_type="application/json",
                body='{"error": "Internal Server Error"}'
                )

    page.route("**/data/company_logos.json", handle_route)

    page.goto("https://reqres.in/")

    logo_link = page.locator(".rr-logo")

    assert logo_link.count() == 0

    assert page.title() == "ReqRes | Free REST API for developers | ReqRes"

    