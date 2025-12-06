from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from report.models import SalaryReport, Operation
from report.forms import SalaryReportCreateForm
from report.filters import SalaryReportFilter, OperationListFilter
from shop.permissions import IsAdminRolePermission


class SalaryReportListView(IsAdminRolePermission, ListView):
    template_name = 'report/pages/salary_report_list.html'
    paginate_by = 10
    model = SalaryReport

    def get_queryset(self):
        user = self.request.user
        if user.is_branch_admin():
            return SalaryReport.objects.filter(branch_office=self.request.user.branch_office).order_by('-id')
        elif user.is_shop_admin():
            return SalaryReport.objects.filter(shop=self.request.user.shop).order_by('-id')

    def get(self, request, *args, **kwargs):
        f = SalaryReportFilter(data=request.GET, queryset=self.get_queryset().all(), request=request)
        self.object_list = f.qs
        context = self.get_context_data(f=f)
        return self.render_to_response(context)


class SalaryReportCreateView(IsAdminRolePermission, CreateView):
    template_name = 'report/forms/salary_report_create.html'
    form_class = SalaryReportCreateForm
    model = SalaryReport
    success_url = reverse_lazy('report:salary_report_list')

    def get_form_kwargs(self):
        user = self.request.user
        form_kwargs = super().get_form_kwargs()
        form_kwargs['shop_id'] = user.shop.id if user.is_shop_admin() else None
        form_kwargs['branch_id'] = user.branch_office.id if user.is_branch_admin() else None
        return form_kwargs


class SalaryReportDeleteView(IsAdminRolePermission, DeleteView):
    model = SalaryReport
    success_url = reverse_lazy('report:salary_report_list')
    template_name = 'report/forms/salary_report_delete.html'


class OperationListView(IsAdminRolePermission, ListView):
    template_name = 'report/pages/operation_list.html'
    filter_class = OperationListFilter
    model = Operation
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        f = self.filter_class(request.GET, self.get_queryset(), request=request)
        self.object_list = f.qs
        context = self.get_context_data(**self.extra_context_data(f=f))
        return self.render_to_response(context)

    def extra_context_data(self, **kwargs) -> dict:
        extra_data = {}
        amount = self.object_list.aggregate(
            sale_amount=Sum('sum_product'),
            profit_amount=Sum('net_profit')
        )
        extra_data.update(amount, **kwargs)
        return extra_data

    def get_queryset(self):
        user = self.request.user
        if user.is_branch_admin():
            queryset = self.model.objects.filter(seller__branch_office=self.request.user.branch_office)
        elif user.is_shop_admin():
            queryset = self.model.objects.filter(seller__shop=self.request.user.shop)
        return queryset.order_by('-id')
