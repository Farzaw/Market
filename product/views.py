from django.shortcuts import get_object_or_404
from django.db.models import Sum, F
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import DeletionMixin

from account.models import User
from product.filters import ProductFilter
from product.models import Product, ProductCategory, ProductInquiry, Provider
from product.forms import (
    ProductCreateForm, ProductUpdateForm, CategoryProductCreateForm, ProviderCreateForm, ProviderUpdateForm)

from shop.permissions import IsAdminRolePermission, ShopAdminPermission


class ProductListView(ShopAdminPermission, ListView):
    template_name = 'product/pages/product_list.html'
    model = Product

    def get_queryset(self):
        return self.request.user.shop.branch_office.all()


class ProductCreateView(IsAdminRolePermission, CreateView):
    template_name = 'product/forms/product_create.html'
    form_class = ProductCreateForm
    model = Product

    def get_form_kwargs(self):
        form = super(ProductCreateView, self).get_form_kwargs()
        try:
            form['shop_id'] = self.request.user.shop.id
        except User.shop.RelatedObjectDoesNotExist:
            form['shop_id'] = self.request.user.branch_office.shop.id
        form['branch_office_id'] = self.kwargs.get('branch_id')
        return form

    def get_success_url(self):
        success_url = reverse('product:product_branch_list', kwargs={'branch_id': self.kwargs.get('branch_id')})
        return success_url


class ProductUpdateView(IsAdminRolePermission, UpdateView):
    template_name = 'product/forms/product_update.html'
    model = Product
    form_class = ProductUpdateForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        num_pack = self.get_object().number_packages
        form = self.get_form()
        if form.is_valid():
            if not int(num_pack) == int(form.data['number_packages']):
                self.object.update_date_quantity = timezone.now()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        form = super().get_form_kwargs()
        form['shop_id'] = self.request.user.shop.id or self.request.user.branch_office.shop.id
        form['branch_office'] = form.get('instance').branch_office
        return form

    def get_success_url(self):
        return reverse('product:product_branch_list', kwargs={'branch_id': self.object.branch_office.id})


class ProductDeleteView(IsAdminRolePermission, DeleteView):
    template_name = 'product/forms/product_delete.html'
    model = Product

    def get_success_url(self):
        return reverse('product:product_branch_list', kwargs={'branch_id': self.object.branch_office.id})


class ProductBranchListView(IsAdminRolePermission, ListView):
    template_name = 'product/pages/product_branch_list.html'
    pk_url_kwarg = 'branch_id'
    paginate_by = 15
    model = Product
    filter_class = ProductFilter

    def get(self, request, *args, **kwargs):
        filter_queryset = self.filter_class(request.GET, queryset=self.get_queryset())
        sum_datas = filter_queryset.qs.aggregate(cost_price__sum=Sum(F('cost_price') * F('number_packages')),
                                                 profit__sum=Sum(F('profit') * F('number_packages')))
        self.object_list = filter_queryset.qs
        context = self.get_context_data(
            f=filter_queryset,
            branch_id=self.kwargs.get(self.pk_url_kwarg),
            providers=self.request.user.shop.provider.all(),
            sum_cost_price=sum_datas.get('cost_price__sum'),
            sum_profit=sum_datas.get('profit__sum')
        )
        return self.render_to_response(context)

    def get_queryset(self):
        return self.model.objects.filter(branch_office=self.kwargs.get(self.pk_url_kwarg)).order_by('-id')


class CategoryProductListView(ShopAdminPermission, ListView):
    template_name = 'product/pages/category_product_list.html'
    model = ProductCategory

    def get_queryset(self):
        return self.model.objects.filter(shop=self.request.user.shop).order_by('-id')


class CategoryProductCreateView(ShopAdminPermission, CreateView):
    template_name = 'product/forms/category_product_create.html'
    form_class = CategoryProductCreateForm
    success_url = reverse_lazy('product:category_product_list')
    model = ProductCategory

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['shop_id'] = self.request.user.shop.id or self.request.user.branch_office.shop_id
        return form_kwargs


class CategoryProductDeleteView(ShopAdminPermission, DeleteView):
    template_name = 'product/forms/category_product_delete.html'
    success_url = reverse_lazy('product:category_product_list')
    model = ProductCategory


class ProductInquiryListView(ListView):
    template_name = 'product/pages/product_inquiry_list.html'
    model = ProductInquiry

    def get(self, request, *args, **kwargs):
        self.get_queryset().update(is_read=True)
        if request.session.get('product_inquiry'):
            del request.session['product_inquiry']
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(branch_office__shop=self.request.user.shop)


class ProductInquiryDeleteView(View, DeletionMixin):
    success_url = reverse_lazy('product:product_inquiry_list')
    model = ProductInquiry

    def get_object(self):
        return get_object_or_404(self.model, id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProviderListView(ListView):
    template_name = 'product/pages/provider_list.html'
    model = Provider

    def get_queryset(self):
        return self.request.user.shop.provider.all()


class ProviderCreateView(CreateView):
    template_name = 'product/forms/provider_create.html'
    model = Provider
    form_class = ProviderCreateForm
    success_url = reverse_lazy('product:provider_list')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['shop_id'] = self.request.user.shop.id
        return form_kwargs


class ProviderUpdateView(UpdateView):
    template_name = 'product/forms/provider_update.html'
    model = Provider
    form_class = ProviderUpdateForm
    success_url = reverse_lazy('product:provider_list')


class ProviderDeleteView(View, DeletionMixin):
    success_url = reverse_lazy('product:provider_list')
    model = Provider

    def get_object(self):
        return get_object_or_404(self.model, id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
