import django_filters

from report.models import SalaryReport, Operation
from account.models import Employee


def employee_filter(request):
    user = request.user
    if user.is_branch_admin():
        return Employee.objects.filter(branch_office=request.user.branch_office)
    elif user.is_shop_admin():
        return Employee.objects.filter(branch_office__shop=request.user.shop)


class SalaryReportFilter(django_filters.FilterSet):
    worker = django_filters.ModelChoiceFilter(queryset=employee_filter)

    class Meta:
        model = SalaryReport
        fields = ('id',)


class OperationListFilter(django_filters.FilterSet):
    date_issue_gte = django_filters.DateTimeFilter(field_name='date_issue',
                                                   method='filter_date_issue_gte',
                                                   label='C')
    date_issue_lte = django_filters.DateTimeFilter(field_name='date_issue',
                                                   method='filter_date_issue_lte',
                                                   label='До')
    seller = django_filters.ModelChoiceFilter(queryset=employee_filter)

    def filter_date_issue_gte(self, queryset, name, value):
        return queryset.filter(date_issue__year__gte=value.year,
                               date_issue__month__gte=value.month,
                               date_issue__day__gte=value.day,)

    def filter_date_issue_lte(self, queryset, name, value):
        return queryset.filter(date_issue__year__lte=value.year,
                               date_issue__month__lte=value.month,
                               date_issue__day__lte=value.day
                               )

    class Meta:
        model = Operation
        fields = ('id', 'seller', 'date_issue_gte', 'date_issue_lte')
