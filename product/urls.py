from django.urls import path

from product.views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    ProductBranchListView, CategoryProductListView, CategoryProductCreateView, CategoryProductDeleteView, \
    ProductInquiryListView, ProductInquiryDeleteView, ProviderListView, ProviderCreateView, ProviderDeleteView, \
    ProviderUpdateView

app_name = 'product'

urlpatterns = [
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/create/<int:branch_id>/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    path('product/branch/<int:branch_id>/list/', ProductBranchListView.as_view(), name='product_branch_list'),

    path('category/product/list/', CategoryProductListView.as_view(), name='category_product_list'),
    path('category/product/create/', CategoryProductCreateView.as_view(), name='category_product_create'),
    path('category/product/delete/<int:pk>/', CategoryProductDeleteView.as_view(), name='category_product_delete'),

    path('product/inquiry/list/', ProductInquiryListView.as_view(), name='product_inquiry_list'),
    path('product/inquiry/delete/<int:pk>/', ProductInquiryDeleteView.as_view(), name='product_inquiry_list'),

    path('provider/list/', ProviderListView.as_view(), name='provider_list'),
    path('provider/create/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
]
