from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from playwright.sync_api import expect
import pytest

def test_cart_is_empty_by_default(page):
    page.goto("https://www.saucedemo.com")

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    assert inventory_page.get_cart_count() == 0

def test_add_item_increases_cart_count(page):
    page.goto("https://www.saucedemo.com")

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    inventory_page.add_first_item_to_cart()

    expect(inventory_page.cart_badge).to_contain_text("1")

def test_sort_by(page):
    page.goto("https://www.saucedemo.com")

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    inventory_page.sort_by("lohi")

    prices = inventory_page.get_item_prices()
    assert prices == sorted(prices)


def test_inventory_shows_six_items(page):
    page.goto("https://www.saucedemo.com")

    login_page = LoginPage(page)

    inventory_page = InventoryPage(page)
    login_page.login("standard_user","secret_sauce")

    assert inventory_page.get_item_count() == 6



@pytest.mark.parametrize("product_name", ["Sauce Labs Backpack", "Sauce Labs Bike Light"])
def test_verify_products_exist(page, product_name):
    page.goto("https://www.saucedemo.com")

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.login("standard_user","secret_sauce")

    assert product_name in inventory_page.get_item_names()

def test_no_product_name_is_blank(page):

    page.goto("https://www.saucedemo.com")

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    
    login_page.login("standard_user","secret_sauce")

    names = inventory_page.get_item_names()

    for name in names:
        assert name != ""

def test_no_duplicate_product_names(page):
    page.goto("https://www.saucedemo.com")

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.login("standard_user","secret_sauce")

    names = inventory_page.get_item_names()
    assert len(names) == len(set(names))

