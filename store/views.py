from django.shortcuts import render
from store.models import Product, Order, ProductDetail, Address
from django.db.models import Sum, F, Avg, Count, IntegerField, DurationField, ExpressionWrapper
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def info_(request):
    total_price = Product.objects.aggregate(total_price=Sum(F('price') * F('quantity')))['total_price']
    list_avg_price = []
    # for item in Product.objects.values('category__name').annotate(avg_price_by_cat=Avg('price')).values('category__name', 'avg_price_by_cat'):
    #     list_avg_price.append(f'<h3>{item['category__name']}, {item['avg_price_by_cat']}</h3>')
    most_expensive_product = Product.objects.order_by('-price').first()
    most_cheap_product = Product.objects.order_by('price').first()
    avg_price = Product.objects.values('category__name').annotate(avg_price_by_cat=Avg('price')).values('category__name', 'avg_price_by_cat')
    count_sum_orders_per_cli = Order.objects.values('customer__first_name', 'customer__last_name').annotate(
        order_count=Count('id', distinct=True), order_total_sum=Sum(F('items__price') * F('items__quantity'))
    ).values('customer__first_name', 'customer__last_name', 'order_count', 'order_total_sum')
    weight_per_cat = (Product.objects.values('category__name').annotate(product_weight_sum=Sum('detail__weight'))
                      .values('category__name', 'product_weight_sum'))
    count_pr_per_supplier = Product.objects.values('supplier__name').annotate(
        pr_per_supp=Count('id')).values('supplier__name', 'pr_per_supp')
    avg_prod_terms = ProductDetail.objects.aggregate(avg_term_by_prod_date=Avg(
        ExpressionWrapper(F('expiration_date') - F('manufacturing_date'), output_field=DurationField())))['avg_term_by_prod_date']
    all_prods_desc = Product.objects.order_by('-price').all()
    sort_orders_by_total_pr = Order.objects.annotate(total_price=Sum(F('items__price') * F('items__quantity'))).order_by('-total_price')
    sort_address_by_country_city = Address.objects.order_by('country', 'city')
    sort_orders_by_orderitem_quantity = Order.objects.annotate(orderitem_count=Count('items__id')).order_by('-orderitem_count')
    all_orders_last_month = Order.objects.filter(order_date__gt=timezone.now() - relativedelta(months=1))
    first_five_prods = Product.objects.all()[:5]
    exp_ten_prods = Product.objects.order_by('-price')[:10]
    return render(request, 'tasks.html', context={'total_price': total_price,
                                                               'avg_price': avg_price,
                                                               'most_exp_prod': most_expensive_product,
                                                               'most_cheap_prod': most_cheap_product,
                                                               'count_sum_per_order': count_sum_orders_per_cli,
                                                               'product_weight_sum': weight_per_cat,
                                                               'count_pr_per_supplier': count_pr_per_supplier,
                                                               'avg_prod_terms': avg_prod_terms,
                                                               'all_prods_desc': all_prods_desc,
                                                               'sort_orders_by_total_pr': sort_orders_by_total_pr,
                                                               'sort_address_by_country_city': sort_address_by_country_city,
                                                               'sort_orders_by_orderitem_quantity': sort_orders_by_orderitem_quantity,
                                                               'all_orders_last_month': all_orders_last_month,
                                                               'first_five_prods': first_five_prods,
                                                               'exp_ten_prods': exp_ten_prods})
