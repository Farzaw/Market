from django.db.models.aggregates import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib import messages

from shop.models import BranchOffice, Position
from shop.forms import BranchCreateForm, BranchUpdateForm, PositionCreateForm
from shop.permissions import ShopAdminPermission, IsAdminRolePermission
from report.models import Operation, ProductOperation
from product.models import ProductInquiry


""" Main page """


class IndexView(IsAdminRolePermission, TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_shop_admin():
            context['income'] = self.request.user.shop.operation.aggregate(income=Sum('sum_product'))['income']
            queryset = ProductOperation.objects.filter(operation__shop=self.request.user.shop)
            context['product_count'] = queryset.aggregate(product_count=Sum('quantity_package'))['product_count']
            product_inquiry = ProductInquiry.objects.filter(
                branch_office__shop=self.request.user.shop, is_read=False
            ).count()
            if product_inquiry:
                request.session['product_inquiry'] = product_inquiry

        elif request.user.is_branch_admin():
            context['income'] = self.request.user.branch_office.operation.aggregate(income=Sum('sum_product'))['income']
            queryset = ProductOperation.objects.filter(operation__branch_office=self.request.user.branch_office)
            context['product_count'] = queryset.aggregate(product_count=Sum('quantity_package'))['product_count']
        return self.render_to_response(context)


""" Branch Office CRUD """


class BranchListView(ShopAdminPermission, ListView):
    template_name = 'branch_office/pages/branch_list.html'
    model = BranchOffice

    def get_queryset(self):
        return self.request.user.shop.branch_office.all()


class BranchCreateView(ShopAdminPermission, CreateView):
    template_name = 'branch_office/forms/branch_create.html'
    form_class = BranchCreateForm
    success_url = reverse_lazy('shop:branch_list')
    model = BranchOffice

    def get_form_kwargs(self):
        kwargs = super(BranchCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'Успешно создан!')
        return super().get_success_url()


class BranchDetailView(IsAdminRolePermission, DetailView):
    template_name = 'branch_office/pages/branch_detail.html'
    pk_url_kwarg = 'branch_id'
    model = BranchOffice

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['income'] = self.object.operation.aggregate(income=Sum('sum_product'))['income']
        queryset = ProductOperation.objects.filter(operation__branch_office=self.kwargs.get(self.pk_url_kwarg))
        context_data['product_count'] = queryset.aggregate(product_count=Sum('quantity_package'))['product_count']
        return context_data


class BranchUpdateView(ShopAdminPermission, UpdateView):
    template_name = "branch_office/forms/branch_update.html"
    pk_url_kwarg = 'branch_id'
    form_class = BranchUpdateForm
    success_url = reverse_lazy('shop:branch_list')
    model = BranchOffice

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['view'] = self
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'Успешно обновлено!')
        return super().get_success_url()


class BranchDeleteView(ShopAdminPermission, DeleteView):
    template_name = 'branch_office/forms/branch_delete.html'
    model = BranchOffice
    pk_url_kwarg = 'branch_id'
    success_url = reverse_lazy('shop:branch_list')

    def get_success_url(self):
        messages.success(self.request, 'Успешно удалено!')
        return super().get_success_url()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.owner.delete(), self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


""" Position CRUD """


class PositionListView(ShopAdminPermission, ListView):
    template_name = 'position/pages/position_list.html'
    model = Position

    def get_queryset(self):
        return self.request.user.shop.position.all()


class PositionCreateView(ShopAdminPermission, CreateView):
    template_name = 'position/forms/position_create.html'
    model = Position
    success_url = reverse_lazy('shop:position_list')
    form_class = PositionCreateForm

    def get_form_kwargs(self):
        kwargs = super(PositionCreateView, self).get_form_kwargs()
        kwargs['shop'] = self.request.user.shop
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'Успешно создан!')
        return super(PositionCreateView, self).get_success_url()


class PositionDeleteView(ShopAdminPermission, DeleteView):
    template_name = 'position/forms/position_delete.html'
    model = Position
    success_url = reverse_lazy('shop:position_list')

    def get_success_url(self):
        messages.success(self.request, 'Успешно удалено!')
        return super(PositionDeleteView, self).get_success_url()
