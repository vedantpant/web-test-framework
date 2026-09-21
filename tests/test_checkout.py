from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage
from pages.cart_page import CartPage
from playwright.sync_api import expect

def test_checkout_with_fake_data(page):
    page.goto("https://www.saucedemo.com")
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    checkout_page = CheckoutPage(page)
    cart_page = CartPage(page)

    login_page.login("standard_user", "secret_sauce")
    inventory_page.add_first_item_to_cart()
    inventory_page.cart_link.click()

    cart_page.checkout_button.click()

    checkout_page.fill_checkout_info()

    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")



