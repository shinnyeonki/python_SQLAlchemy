import faker

fake = faker.Faker('ko_KR')



for _ in range(10):
    print(fake.name(), fake.email(), fake.address(), fake.company(), fake.job(), fake.phone_number())