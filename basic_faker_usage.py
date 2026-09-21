from faker import Faker

fake = Faker()

for i in range(3):
    print(fake.first_name())
    print(fake.last_name())
    print(fake.zipcode())
    print(fake.email())