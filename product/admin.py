from django.contrib import admin

from product.models import Product, ProductCategory, ProductInquiry, Provider


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_branch_name')
    list_display_links = ('id', 'name',)

    def get_branch_name(self, obj):
        return obj.branch_office.name


@admin.register(ProductInquiry)
class ProductInquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch_office', 'product')
    list_display_links = ('id', 'branch_office')
