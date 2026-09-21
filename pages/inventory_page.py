class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.add_to_cart_backpack = page.locator('[data-test="add-to-cart-sauce-labs-backpack"]')
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.item_price = page.locator('[data-test="inventory-item-price"]')
        self.inventory_item = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        

    def add_first_item_to_cart(self):
        self.add_to_cart_backpack.click()

    def get_cart_count(self):
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.text_content())

    def sort_by(self, option_value):
        self.sort_dropdown.select_option(option_value)

    def get_item_prices(self):
        item_prices = self.item_price.all_inner_texts()
        prices = []

        for item in item_prices:
            price = float(item.replace("$", ""))
            prices.append(price)

        return prices

    def get_item_count(self):
        return self.inventory_item.count()

    def get_item_names(self):
        return self.item_names.all_inner_texts()
        


