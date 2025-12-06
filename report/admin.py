from django.contrib import admin

from report.models import Operation, SalaryReport, ProductOperation


@admin.register(SalaryReport)
class SalaryReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch_office', 'worker')
    list_display_links = ('id', 'branch_office', 'worker')


class ProductOperationInline(admin.TabularInline):
    model = ProductOperation
    readonly_fields = ('name', 'price', 'piece_price', 'quantity_package', 'quantity_piece', 'sum', 'barcode')
    verbose_name = 'Продукт'
    verbose_name_plural = 'Продукты'
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj):
        return False


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'sum_product', 'money_received', 'change', 'date_issue')
    list_display_links = ('seller',)
    list_filter = ('date_issue',)
    inlines = [ProductOperationInline]
