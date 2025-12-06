import django_filters

from product.models import Product


class ProductFilter(django_filters.FilterSet):
    update_date_quantity_gte = django_filters.DateTimeFilter(field_name='update_date_quantity',
                                                   method='filter_update_date_quantity_gte',
                                                   label='C')
    update_date_quantity_lte = django_filters.DateTimeFilter(field_name='update_date_quantity',
                                                   method='filter_update_date_quantity_lte',
                                                   label='До')

    def filter_update_date_quantity_gte(self, queryset, name, value):
        return queryset.filter(update_date_quantity__year__gte=value.year,
                               update_date_quantity__month__gte=value.month,
                               update_date_quantity__day__gte=value.day,)

    def filter_update_date_quantity_lte(self, queryset, name, value):
        return queryset.filter(update_date_quantity__year__lte=value.year,
                               update_date_quantity__month__lte=value.month,
                               update_date_quantity__day__lte=value.day)

    class Meta:
        model = Product
        fields = ('name', 'barcode', 'provider', 'update_date_quantity')
