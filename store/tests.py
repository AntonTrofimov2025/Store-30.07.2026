from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from store.models import Category, Supplier, Product


class Tests(APITestCase):

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

    def test_product_create(self):
        self.test_create_category()
        self.test_create_supplier()
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

