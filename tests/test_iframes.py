from playwright.sync_api import Page, expect

IFRAME_PAGE_URL = "https://the-internet.herokuapp.com/iframe"
IFRAME_SELECTOR = "#mce_0_ifr"
EDITOR_BODY = "#tinymce"
TEXT = "Hello from Playwright"

def test_type_text_inside_iframe(page:Page):
    page.goto(IFRAME_PAGE_URL)

    frame = page.frame_locator(IFRAME_SELECTOR)
    editor = frame.locator(EDITOR_BODY)

    editor.fill(TEXT)

    expect(editor).to_have_text(TEXT)


