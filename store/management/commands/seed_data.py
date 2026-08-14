"""
Management command: seed_data

Generates fake data for the store application:
Category, Supplier, Product, ProductDetail,
Address, Customer, Order, OrderItem.

Usage:
    python manage.py seed_data

    python manage.py seed_data \
        --categories 10 \
        --suppliers 15 \
        --products 100 \
        --addresses 50 \
        --customers 80 \
        --orders 150 \
        --order-items 400

    python manage.py seed_data --flush

Requires Faker:
    pip install Faker
"""

import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from faker import Faker

from store.models import (
    Address,
    Category,
    Customer,
    Order,
    OrderItem,
    Product,
    ProductDetail,
    Supplier,
)


fake = Faker()


CATEGORY_NAMES = [
    "Электроника",
    "Бытовая техника",
    "Одежда",
    "Обувь",
    "Аксессуары",
    "Дом и сад",
    "Спорт",
    "Красота",
    "Канцелярия",
    "Автотовары",
]

COUNTRIES = [
    "Romania",
    "Germany",
    "France",
    "Italy",
    "Spain",
    "Poland",
    "Czech Republic",
    "Austria",
]


class Command(BaseCommand):
    help = "Generates fake data for the store application."

    def add_arguments(self, parser):
        parser.add_argument(
            "--categories",
            type=int,
            default=8,
            help="Number of categories to create.",
        )
        parser.add_argument(
            "--suppliers",
            type=int,
            default=10,
            help="Number of suppliers to create.",
        )
        parser.add_argument(
            "--products",
            type=int,
            default=50,
            help="Number of products to create.",
        )
        parser.add_argument(
            "--product-details",
            type=int,
            default=None,
            help=(
                "Number of ProductDetail objects to create. "
                "By default, one detail is created for every product."
            ),
        )
        parser.add_argument(
            "--addresses",
            type=int,
            default=25,
            help="Number of addresses to create.",
        )
        parser.add_argument(
            "--customers",
            type=int,
            default=30,
            help="Number of customers to create.",
        )
        parser.add_argument(
            "--orders",
            type=int,
            default=50,
            help="Number of orders to create.",
        )
        parser.add_argument(
            "--order-items",
            type=int,
            default=None,
            help=(
                "Number of OrderItem objects to create. "
                "By default, approximately 2 items per order."
            ),
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing store data before generating new data.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            self._flush()

        with transaction.atomic():
            categories = self._create_categories(
                options["categories"]
            )

            suppliers = self._create_suppliers(
                options["suppliers"]
            )

            products = self._create_products(
                options["products"],
                categories,
                suppliers,
            )

            product_details_count = options["product_details"]

            if product_details_count is None:
                product_details_count = len(products)

            product_details = self._create_product_details(
                product_details_count,
                products,
            )

            addresses = self._create_addresses(
                options["addresses"]
            )

            customers = self._create_customers(
                options["customers"],
                addresses,
            )

            orders = self._create_orders(
                options["orders"],
                customers,
            )

            order_items = self._create_order_items(
                options["order_items"],
                orders,
                products,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Done:\n"
                f"  categories: {len(categories)}\n"
                f"  suppliers: {len(suppliers)}\n"
                f"  products: {len(products)}\n"
                f"  product details: {len(product_details)}\n"
                f"  addresses: {len(addresses)}\n"
                f"  customers: {len(customers)}\n"
                f"  orders: {len(orders)}\n"
                f"  order items: {len(order_items)}"
            )
        )

    # ------------------------------------------------------------------ #
    # Flush
    # ------------------------------------------------------------------ #

    def _flush(self):
        self.stdout.write(
            self.style.WARNING(
                "Deleting existing store data..."
            )
        )

        # Удаляем от зависимых моделей к независимым.

        # OrderItem -> Order / Product
        OrderItem.objects.all().delete()

        # Order -> Customer
        Order.objects.all().delete()

        # Customer -> Address (SET_NULL)
        Customer.objects.all().delete()

        # ProductDetail -> Product
        ProductDetail.objects.all().delete()

        # Product -> Category / Supplier
        Product.objects.all().delete()

        Supplier.objects.all().delete()
        Category.objects.all().delete()

        Address.objects.all().delete()

    # ------------------------------------------------------------------ #
    # Category
    # ------------------------------------------------------------------ #

    def _create_categories(self, count):
        if count <= 0:
            return []

        categories = []

        names = CATEGORY_NAMES[:]
        random.shuffle(names)

        # Используем готовые названия.
        for name in names[:count]:
            category, _ = Category.objects.get_or_create(
                name=name
            )
            categories.append(category)

        # Если count больше количества готовых названий,
        # генерируем дополнительные уникальные категории.
        while len(categories) < count:
            name = fake.unique.word().capitalize()

            category, created = Category.objects.get_or_create(
                name=name
            )

            if created:
                categories.append(category)

        return categories

    # ------------------------------------------------------------------ #
    # Supplier
    # ------------------------------------------------------------------ #

    def _create_suppliers(self, count):
        if count <= 0:
            return []

        suppliers = []

        for _ in range(count):
            supplier = Supplier.objects.create(
                name=fake.company()[:150],
                contact_email=fake.unique.email(),
                phone_number=fake.phone_number()[:20],
            )

            suppliers.append(supplier)

        return suppliers

    # ------------------------------------------------------------------ #
    # Product
    # ------------------------------------------------------------------ #

    def _create_products(
        self,
        count,
        categories,
        suppliers,
    ):
        if count <= 0:
            return []

        if not categories or not suppliers:
            self.stdout.write(
                self.style.WARNING(
                    "No categories or suppliers — "
                    "skipping products."
                )
            )
            return []

        products = []

        for _ in range(count):
            quantity = fake.random_int(
                min=0,
                max=250,
            )

            price = (
                Decimal(
                    fake.random_int(
                        min=100,
                        max=500000,
                    )
                )
                / Decimal("100")
            )

            product = Product.objects.create(
                name=fake.catch_phrase()[:200],
                category=random.choice(categories),
                supplier=random.choice(suppliers),
                price=price,
                quantity=quantity,
                article=self._generate_article(),
                available=quantity > 0,
            )

            products.append(product)

        return products

    # ------------------------------------------------------------------ #
    # ProductDetail
    # ------------------------------------------------------------------ #

    def _create_product_details(
        self,
        count,
        products,
    ):
        if count <= 0 or not products:
            return []

        selected_products = random.sample(
            products,
            k=min(count, len(products)),
        )

        details = []

        for product in selected_products:
            manufacturing_date = fake.date_between(
                start_date="-3y",
                end_date="today",
            )

            # У большинства товаров есть срок годности,
            # но для части товаров оставляем NULL.
            if random.random() < 0.8:
                expiration_date = (
                    manufacturing_date
                    + timedelta(
                        days=random.randint(
                            30,
                            1095,
                        )
                    )
                )
            else:
                expiration_date = None

            weight = (
                Decimal(
                    fake.random_int(
                        min=50,
                        max=50000,
                    )
                )
                / Decimal("1000")
            )

            detail = ProductDetail.objects.create(
                product=product,
                description=fake.paragraph(
                    nb_sentences=4
                ),
                manufacturing_date=manufacturing_date,
                expiration_date=expiration_date,
                weight=weight,
            )

            details.append(detail)

        return details

    # ------------------------------------------------------------------ #
    # Address
    # ------------------------------------------------------------------ #

    def _create_addresses(self, count):
        if count <= 0:
            return []

        addresses = []

        for _ in range(count):
            address = Address.objects.create(
                country=random.choice(COUNTRIES),
                city=fake.city()[:100],
                street=fake.street_name()[:150],
                house=str(
                    fake.random_int(
                        min=1,
                        max=250,
                    )
                ),
            )

            addresses.append(address)

        return addresses

    # ------------------------------------------------------------------ #
    # Customer
    # ------------------------------------------------------------------ #

    def _create_customers(
        self,
        count,
        addresses,
    ):
        if count <= 0:
            return []

        customers = []

        for _ in range(count):
            customer = Customer.objects.create(
                first_name=fake.first_name()[:100],
                last_name=fake.last_name()[:100],
                email=fake.unique.email(),
                phone_number=fake.phone_number()[:20],
                address=(
                    random.choice(addresses)
                    if addresses
                    else None
                ),
            )

            customers.append(customer)

        return customers

    # ------------------------------------------------------------------ #
    # Order
    # ------------------------------------------------------------------ #

    def _create_orders(
        self,
        count,
        customers,
    ):
        if count <= 0:
            return []

        if not customers:
            self.stdout.write(
                self.style.WARNING(
                    "No customers — skipping orders."
                )
            )
            return []

        orders = []

        for _ in range(count):
            naive_order_date = fake.date_time_between(
                start_date="-1y",
                end_date="now",
            )

            if timezone.is_aware(timezone.now()):
                order_date = timezone.make_aware(
                    naive_order_date
                )
            else:
                order_date = naive_order_date

            order = Order.objects.create(
                customer=random.choice(customers),
                order_date=order_date,
            )

            orders.append(order)

        return orders

    # ------------------------------------------------------------------ #
    # OrderItem
    # ------------------------------------------------------------------ #

    def _create_order_items(
        self,
        requested_count,
        orders,
        products,
    ):
        if not orders or not products:
            self.stdout.write(
                self.style.WARNING(
                    "No orders or products — "
                    "skipping order items."
                )
            )
            return []

        if requested_count is None:
            requested_count = len(orders) * 2

        if requested_count <= 0:
            return []

        # В модели нет unique constraint для order/product,
        # но для реалистичных тестовых данных не будем
        # добавлять один и тот же товар дважды в один заказ.
        max_possible = len(orders) * len(products)

        target_count = min(
            requested_count,
            max_possible,
        )

        items = []
        used_pairs = set()

        attempts = 0
        max_attempts = max(
            target_count * 10,
            100,
        )

        while (
            len(items) < target_count
            and attempts < max_attempts
        ):
            attempts += 1

            order = random.choice(orders)
            product = random.choice(products)

            pair = (
                order.pk,
                product.pk,
            )

            if pair in used_pairs:
                continue

            used_pairs.add(pair)

            item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=random.randint(1, 10),
                price=product.price,
            )

            items.append(item)

        if len(items) < target_count:
            self.stdout.write(
                self.style.WARNING(
                    f"Created {len(items)} of "
                    f"{target_count} requested order items."
                )
            )

        return items

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _generate_article():
        """
        Generates a unique-looking product article.

        Example:
            AB-381245

        Product.article has:
            max_length=50
            unique=True
        """

        return (
            f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
            f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
            f"-{random.randint(100000, 999999)}"
        )