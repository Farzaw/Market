from django.contrib import admin

from shop.models import Shop, BranchOffice, Category, PhotoDocument, Position
from account.models import Employee
from product.models import Product


class BranchOfficeInline(admin.TabularInline):
    model = BranchOffice
    extra = 1


class PhotoDocumentInline(admin.TabularInline):
    model = PhotoDocument
    extra = 1


class PositionInline(admin.TabularInline):
    model = Position
    extra = 1


class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 1


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')
    list_display_links = ('name',)
    inlines = (BranchOfficeInline, PositionInline, PhotoDocumentInline)


@admin.register(BranchOffice)
class BranchOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'name', 'owner')
    list_display_links = ('name',)
    inlines = (EmployeeInline, ProductInline)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


@admin.register(PhotoDocument)
class PhotoDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'image')
    list_display_links = ('shop',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'shop')
    list_display_links = ('name',)
