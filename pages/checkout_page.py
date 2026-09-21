from faker import Faker

class CheckoutPage:
    def __init__(self,page):
        self.page = page
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_to_checkout = page.locator('[data-test="continue"]')
        self.fake = Faker()

    def fill_checkout_info(self):
        self.first_name.fill(self.fake.first_name())
        self.last_name.fill(self.fake.last_name())
        self.postal_code.fill(self.fake.zipcode())
        self.continue_to_checkout.click()