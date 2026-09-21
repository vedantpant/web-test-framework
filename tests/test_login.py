# def test_saucedemo_title(browser):
#     page = browser.new_page()
#     page.goto("https://www.saucedemo.com")
#     assert page.title().strip() == "Swag Labs"
#     page.close()

from playwright.sync_api import expect
from pages.login_page import LoginPage

def test_standard_user_login(page):
    page.goto("https://www.saucedemo.com")

    login_page = LoginPage(page)
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_invalid_login_shows_error(page):
    
    page.goto("https://www.saucedemo.com")

    login_page = LoginPage(page)
    login_page.login("standard_user", "wrong_password")

    expect(login_page.error_message).to_contain_text("Epic sadface")

# def test_deliberate_failure(page):
#     page.goto("https://www.saucedemo.com")
#     assert page.title() == "This is Wrong On Purpose"