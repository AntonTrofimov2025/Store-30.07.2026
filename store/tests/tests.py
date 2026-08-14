from django.urls import reverse
from rest_framework.test import APITestCase
from store.models import (Category, Supplier, Product, ProductDetail,
                          Address, Customer, Order, OrderItem)
from django.contrib.auth import get_user_model
from faker import Faker
import random
from decimal import Decimal
from string import ascii_uppercase, digits
from django.utils import timezone
from datetime import date, datetime, timedelta

class Tests(APITestCase):

    def setUp(self):
        self.create_db()

    def create_db(self):
        fake = Faker()
        categories = [Category(name=fake.unique.word()) for _ in range(25)]
        Category.objects.bulk_create(categories)
        suppliers = [Supplier(name=fake.unique.word(),
                              contact_email=fake.unique.email(),
                              phone_number=fake.unique.phone_number()) for _ in range(40)]
        Supplier.objects.bulk_create(suppliers)
        products = [Product(name=fake.unique.word(),
                           # price=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                            price=Decimal(random.randint(1, 10000)) / Decimal(100),
                            quantity=random.randint(1, 10000),
                            article=''.join(random.choice(ascii_uppercase) for _ in range(5))
                                    + '-' + ''.join(str(random.choice(digits)) for _ in range(2)),
                            available=random.choice([True, False]),
                            category=random.choice(categories),
                            supplier=random.choice(suppliers)) for _ in range(100)]
        Product.objects.bulk_create(products)
        all_products = list(Product.objects.all())
        random.shuffle(all_products)
        product_details = [ProductDetail(product=all_products.pop(),
                                         description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                                         manufacturing_date=fake.date_between_dates(date(2024, 1, 1),
                                                                                    date(2026, 7, 15)),
                                         expiration_date=fake.date_between_dates(date(2027, 1, 1),
                                                                                 date(2030, 1, 1)),
                                         weight=Decimal(random.randint(1, 100000)) / Decimal(100)) for _ in range(100)]
        ProductDetail.objects.bulk_create(product_details)
        addresses = [Address(country=fake.country(),
                             city=fake.city(),
                             street=fake.street_name(),
                             house=random.randint(1, 50)) for _ in range(200)]
        Address.objects.bulk_create(addresses)
        customers = [Customer(first_name=fake.first_name(),
                  last_name=fake.last_name(),
                  email=fake.unique.email(),
                  phone_number=fake.unique.numerify(text="+###########"),
                  address=random.choice(addresses),
                  date_joined=fake.date_time_between_dates(timezone.make_aware(datetime(2020, 1, 1)),
                                                      timezone.make_aware(datetime(2026, 7, 30))))
                                                                                            for _ in range(100)]
        Customer.objects.bulk_create(customers)
        orders = [Order(customer=random.choice(customers),
                        order_date=fake.date_time_between_dates(timezone.make_aware(datetime(2026, 6, 15)),
                                                           timezone.now() - timedelta(days=3))) for _ in range(100)]
        Order.objects.bulk_create(orders)
        order_items = [OrderItem(order=random.choice(orders),
                                 product=random.choice(products),
                                 quantity=random.randint(1, 100),
                                 price=Decimal(random.randint(1, 10000))/ Decimal(100)) for _ in range(150)]
        OrderItem.objects.bulk_create(order_items)


    def test_create_category(self):
        cat = {'name': 'hey'}
        response = self.client.post(reverse('category-list-create-view'), data=cat, format='json')
        self.assertIsNone(response.data.get('name'))
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data['id'])

    def test_create_supplier(self):
        supp = {'name': 'hey',
        'contact_email': 'dasd@yahoo.com'}
        response = self.client.post(reverse('supplier-list-create-view'), data=supp, format='json')
        self.assertIsNone(response.data.get('name'))
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data['id'])
        get_supplier = Supplier.objects.get(id=response.data['id'])
        self.assertEqual(get_supplier.phone_number, '')

    def test_product_create(self):
        product = {'name': 'hey', 'price': Decimal('122.22'), 'article': 'prod_hey', 'quantity': 5, 'available': True,
                   'category': Category.objects.first().id, 'supplier': Supplier.objects.first().id}
        self.client.post(reverse('product-list-create-view'), data=product, format='json')
        response_list = self.client.get(reverse('product-list-create-view'))
        for product in response_list.data:
            self.assertIn('name', product['category_detail'])
            self.assertIn('name', product['supplier_detail'])
        get_prod = Product.objects.first()
        self.client.put(reverse('product-detail-view', args=[get_prod.id]),
                                   data={'name': 'trulala'}, format='json')
        get_prod.refresh_from_db()
        self.assertEqual(get_prod.name, 'trulala')

