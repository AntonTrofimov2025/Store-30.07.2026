from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from .tests import Tests
from ..models import Category, Supplier, Address, Customer, Order, OrderItem
from core.models import (AddressTypes, CustomerTypes, SupplierStatus,
                         ProductStatus, ProductDetailTypes, OrderStatus)
import random
from string import ascii_uppercase, digits


class TestsViewset(APITestCase):

    def setUp(self):
        Tests.create_db()


    def test_category(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        data = {'name': 'hey'}
        response = self.client.post(reverse('category-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        data = {'name': 'whats up'}
        response = self.client.patch(reverse('category-detail',
                                             args=[response.data['id']]), data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'whats up')

    def test_supplier(self):
        response = self.client.get(reverse('supplier-list'))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        data = {'name': 'hey', 'status': 'av',
                'contact_email': 'dasd@yahoo.com'}
        response = self.client.post(reverse('supplier-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        data = {'name': 'whats up'}
        response = self.client.patch(reverse('supplier-detail',
                                             args=[response.data['id']]), data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'whats up')

    def test_product(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        data = {'name': 'hey', 'price': Decimal('122.22'), 'article': 'prod_hey', 'quantity': 5, 'available': True,
                   'category': Category.objects.first().id, 'supplier': Supplier.objects.first().id,
                'status': 'is'}
        response = self.client.post(reverse('product-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        data = {'name': 'whats up'}
        response = self.client.patch(reverse('product-detail',
                                             args=[response.data['id']]), data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'whats up')
        return response

    def test_product_detail(self):
        prod_detail = {'description': 'dnkasdnasjdnkajsdnjk', 'product': self.test_product().data['id'],
                       'manufacturing_date': '2025-1-1', 'pd_type': 'cp',
                       'expiration_date': '2027-2-2', 'weight': 555}
        response = self.client.post(reverse('product_detail-list'), data=prod_detail, format='json')
        self.assertEqual(response.status_code, 201)

    def test_address(self):
        response = self.client.get(reverse('address-list'))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        data = {'country': 'Deutsches Reich', 'city': '312', 'street': 'Brandenburger Tor', 'house': 4,
                    'address_type': 'hm'}
        response = self.client.post(reverse('address-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        data = {'city': 'Berlin'}
        response = self.client.patch(reverse('address-detail',
                                             args=[response.data['id']]), data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['city'], 'Berlin')

    def test_customer(self):
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, 200)
        gimme_address = Address.objects.first()
        data = {'first_name': 'Johnny', 'last_name': 'Walker',
                'email': 'john_walk@gmail.com',
                'phone_number': '+44555555555',
                'address': gimme_address.id, 'customer_type': 'rg'}
        response = self.client.post(reverse('customer-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        data = {'first_name': 'Mike',
                'phone_number': '+342311323333'}
        response = self.client.patch(reverse('customer-detail', args=[response.data['id']]), data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Mike')
        self.assertEqual(response.data['phone_number'], '+342311323333')
        data = {'first_name': 'Mike PUT', 'last_name': 'Walker',
                'email': 'john_walk@gmail.com',
                'phone_number': '+3423113233332',
                'address': gimme_address.id, 'customer_type': 'rg'}
        response = self.client.put(reverse('customer-detail', args=[response.data['id']]), data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Mike PUT')
        self.assertEqual(response.data['phone_number'], '+3423113233332')

    def test_order(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 200)
        gimme_custmr = Customer.objects.first()
        data = {'customer': gimme_custmr.id, 'status': 'pd'}
        response = self.client.post(reverse('order-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

        our_order = Order.objects.get(id=response.data['id'])
        len_our_order = len(our_order.items.all())
        order_item_1 = OrderItem.objects.first()
        order_item_2 = OrderItem.objects.last()
        our_order.items.add(order_item_1, order_item_2)
        our_order.save()
        our_order.refresh_from_db()
        self.assertEqual(len(our_order.items.all()), len_our_order + 2)

    def test_order_item(self):
        get_order = Order.objects.last()
        prod_data = {'name': 'Best product ever :DD',
                     'price': Decimal(random.randint(1, 10000)) / Decimal(100),
                     'quantity': random.randint(1, 10000),
                     'article': ''.join(random.choice(ascii_uppercase) for _ in range(5))
                                + '-' + ''.join(str(random.choice(digits)) for _ in range(2)),
                     'available': random.choice([True, False]),
                     'category': Category.objects.first().id,
                     'supplier': Supplier.objects.first().id,
                     'status': 'is'}
        response = self.client.post(reverse('product-list'), data=prod_data, format='json')
        self.assertEqual(response.status_code, 201)

        data = {'order': get_order.id,
                'product': response.data['id'],
                'quantity': random.randint(1, 100),
                'price': 50000}
        create_order_item = self.client.post(reverse('order_item-list'), data=data, format='json')
        self.assertEqual(create_order_item.status_code, 201)

    def test_filter_product_category_price(self):
        response = self.client.post(reverse('category-list'), data={'name': 'hey whats up buddy? :)'}, format='json')
        self.assertEqual(response.status_code, 201)
        get_this_cat = Category.objects.get(pk=response.data['id'])

        data = {'name': 'hey', 'price': Decimal('5445.72'), 'article': 'prod_hey', 'quantity': 5, 'available': True,
                'category': get_this_cat.id, 'supplier': Supplier.objects.last().id,
                'status': 'is'}
        response = self.client.post(reverse('product-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('product-list'), query_params={'category': 'hey-whats-up-buddy', 'price': '5445.72'})
        self.assertEqual(response.status_code, 200)
        for prod in response.data['results']:
            self.assertEqual(prod['category_detail']['name'], 'hey whats up buddy? :)')
            self.assertEqual(prod['category_slug'], 'hey-whats-up-buddy')
            self.assertEqual(prod['price'], '5445.72')

    def test_filter_customer_first_last_names(self):
        data = {'first_name': 'Johnny', 'last_name': 'Walker',
                'email': 'john_walk@gmail.com',
                'phone_number': '+44555555555',
                'address': Address.objects.first().id, 'customer_type': 'rg'}
        response = self.client.post(reverse('customer-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('customer-list'), query_params={'first_name': 'Johnny', 'last_name': 'Walker'})
        self.assertEqual(response.status_code, 200)
        for johnny in response.data['results']:
            self.assertEqual(johnny['first_name'], 'Johnny')
            self.assertEqual(johnny['last_name'], 'Walker')

