import time

def test_logos_section_empty_during_slow_load(page):
    def handle_route(route):
        print("\n>>> Mock hanlder triggered <<<")
        page.wait_for_timeout(3000)
        route.fulfill(
            status=200,
            content_type="application/json",
            body='[]'
        )

    page.route("**/data/company_logos.json", handle_route)

    start_time = time.time()
    page.goto("https://reqres.in/")
    page.wait_for_load_state("networkidle")
    elapsed_time = time.time() - start_time
    print(f"\ngoto() took {elapsed_time:.2f} seconds to return")

    logo_link = page.locator(".rr-logo").filter(has_not=page.locator(".rr-logo__cta-text"))
    count = logo_link.count()
    print(f"\n Found {count} logo(s)")
    if count > 0:
        print(f"first logo HTML: {logo_link.first.inner_html()}")
    assert logo_link.count() == 0