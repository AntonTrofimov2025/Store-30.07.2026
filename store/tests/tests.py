from http.client import responses

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
                             house=str(random.randint(1, 50))) for _ in range(200)]
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
                        #order_date=fake.date_time_between_dates(timezone.make_aware(datetime(2026, 6, 15)),
                                                           #timezone.now() - timedelta(days=3))
                        )for _ in range(100)]
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

    def test_create_prod_detail(self):
        product = {'name': 'hey', 'price': Decimal('122.22'), 'article': 'prod_hey', 'quantity': 5, 'available': True,
                   'category': Category.objects.first().id, 'supplier': Supplier.objects.first().id}
        prod_created = self.client.post(reverse('product-list-create-view'), data=product, format='json')
        prod_detail = {'description': 'dnkasdnasjdnkajsdnjk', 'product': prod_created.data['id'],
                       'manufacturing_date': '2025-1-1',
                       'expiration_date': '2027-2-2', 'weight': 555}
        response = self.client.post(reverse('prod_dt-list-create-view'), data=prod_detail, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_prod_detail(self):
        our_product = Product.objects.first()
        upd = {'description': 'hey whats up? :)'}
        response = self.client.patch(reverse('prod_dt-detail-view', args=[our_product.detail.id]), data=upd, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], 'hey whats up? :)')

    def test_address_list(self):
        response = self.client.get(reverse('address-list-create-view'))
        self.assertEqual(response.status_code, 200)

    def test_address_create(self):
        new_addr = {'country': 'Deutsches Reich', 'city': '312', 'street': 'Brandenburger Tor', 'house': 4}
        response = self.client.post(reverse('address-list-create-view'), data=new_addr, format='json')
        self.assertEqual(response.status_code, 201)

    def test_address_update(self):
        get_addr = Address.objects.all().first()
        upd = {'street': 'Brandenburger Tor', 'house': '4'}
        response = self.client.patch(reverse('address-detail-view', args=[get_addr.id]), data=upd, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['street'], 'Brandenburger Tor')
        self.assertEqual(response.data['house'], '4')

    def test_customer_create(self):
        gimme_address = Address.objects.first()
        data = {'first_name': 'Johnny', 'last_name': 'Walker',
                'email': 'john_walk@gmail.com',
                'phone_number': '+44555555555',
                'address': gimme_address.id}
        response = self.client.post(reverse('customer-list-create-view'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_customer_update(self):
        get_smbd = Customer.objects.first()
        data = {'first_name': 'Mike',
                'phone_number': '+342311323333'}
        response = self.client.patch(reverse('customer-detail-view', args=[get_smbd.id]), data=data, format='json')
        self.assertEqual(response.status_code, 200)
        get_smbd.refresh_from_db()
        self.assertEqual(get_smbd.first_name, 'Mike')
        self.assertEqual(get_smbd.phone_number, '+342311323333')

    def test_order_create(self):
        gimme_custmr = Customer.objects.first()
        data = {#'order_date': timezone.make_aware(datetime(2026, 8, 4)).isoformat(),
                'customer': gimme_custmr.id}
        response = self.client.post(reverse('order-list-create-view'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_order_update(self):
        gimme_custmr = Customer.objects.first()
        data = {#'order_date': timezone.make_aware(datetime(2026, 8, 4)).isoformat(),
                'customer': gimme_custmr.id}
        created_order = self.client.post(reverse('order-list-create-view'), data=data, format='json')
        # data = {#'order_date': timezone.make_aware(datetime(2021, 8, 4)).isoformat(),
        #         'customer': gimme_custmr.id}
        # response = self.client.patch(reverse('order-detail-create-view',
        #                                     args=[created_order.data['id']]),
        #                                     data=data, format='json')
        # self.assertEqual(response.status_code, 200)
        our_order = Order.objects.get(id=created_order.data['id'])
        len_our_order = len(our_order.items.all())

        get_order_item = OrderItem.objects.first()
        get_order_item_2 = OrderItem.objects.last()
        our_order.items.add(get_order_item, get_order_item_2)
        our_order.save()
        our_order.refresh_from_db()
        self.assertEqual(len(our_order.items.all()), len_our_order + 2)

        # self.assertIn('2021-08-04', our_order.order_date.isoformat())

    def test_order_item_create(self):
        get_order = Order.objects.first()
        prod_data = {'name': 'Best product ever :DD',
                            'price': Decimal(random.randint(1, 10000)) / Decimal(100),
                            'quantity': random.randint(1, 10000),
                            'article': ''.join(random.choice(ascii_uppercase) for _ in range(5))
                                    + '-' + ''.join(str(random.choice(digits)) for _ in range(2)),
                            'available': random.choice([True, False]),
                            'category': Category.objects.first().id,
                            'supplier': Supplier.objects.first().id}
        create_prod = self.client.post(reverse('product-list-create-view'), data=prod_data, format='json')
        data = {'order': get_order.id,
                'product': create_prod.data['id'],
                'quantity': random.randint(1, 100),
                'price': 50000}
        create_order_item = self.client.post(reverse('order_item-list-create-view'), data=data, format='json')
        self.assertEqual(create_order_item.status_code, 201)

    def test_order_item_wrong_quantity(self):
        data = {'order': Order.objects.last().id,
                'product': Product.objects.last().id,
                'quantity': 1001,
                'price': 50000}
        create_order_item = self.client.post(reverse('order_item-list-create-view'), data=data, format='json')
        self.assertEqual(create_order_item.status_code, 400)
        self.assertIn('Quantity above 1000 is not allowed!!', create_order_item.data['quantity'])

    def test_order_item_update(self):
        get_order_item = OrderItem.objects.first()
        upd = {'quantity': 445,
               'price': 1234}
        response = self.client.patch(reverse('order_item-detail-view', args=[get_order_item.id]),
                                     data=upd, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['quantity'], 445)
        self.assertEqual(response.data['price'], str(Decimal(1234).quantize(Decimal('0.01'))))

    def customer_wrong_phone_number(self, your_number: str):
        gimme_address = Address.objects.first()
        data = {'first_name': 'Johnny', 'last_name': 'Walker',
                'email': 'john_walk@gmail.com',
                'phone_number': your_number,
                'address': gimme_address.id}
        response = self.client.post(reverse('customer-list-create-view'), data=data, format='json')
        self.assertTrue('The phone number must consist of 10-15 symbols in total and start from + symbol!!\n'
                        'Example: +3423234455323' in response.data['phone_number']
                        or 'Ensure this field has no more than 15 characters.' in response.data['phone_number'])

    def test_wrong_number_ohne_plus(self):
        return self.customer_wrong_phone_number('44555555555')

    def test_wrong_number_more_than_15(self):
        return self.customer_wrong_phone_number('+445555555552134')

    def test_wrong_number_with_buchstaben(self):
        return self.customer_wrong_phone_number('+4455d52134')

