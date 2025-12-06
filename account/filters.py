import django_filters

from account.models import Employee, Position


def position_filter(request):
    user = request.user
    shop = user.shop if user.is_shop_admin() else user.branch_office.shop
    return Position.objects.filter(shop=shop)


class EmployeeFilter(django_filters.FilterSet):
    position_id = django_filters.ModelChoiceFilter(queryset=position_filter)

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'phone')
