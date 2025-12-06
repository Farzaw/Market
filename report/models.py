from django.db import models

from config.choices import CurrencyChoices
from product.models import Product
from shop.models import Shop, BranchOffice
from account.models import Employee, CashSession


class SalaryReport(models.Model):
    branch_office: BranchOffice = models.ForeignKey(
        BranchOffice, related_name='salary_report', on_delete=models.CASCADE, verbose_name='Филиал'
    )
    shop: Shop = models.ForeignKey(Shop, related_name='salary_report', on_delete=models.CASCADE, verbose_name='Магазн')
    worker: Employee = models.ForeignKey(
        Employee, related_name='salary_report', on_delete=models.CASCADE, verbose_name='Работник'
    )
    got_money = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Получил денег')
    currency = models.CharField(max_length=32, choices=CurrencyChoices.choices, verbose_name='Валюта')
    date_from = models.DateField(verbose_name='C')
    date_before = models.DateField(verbose_name='До')

    def __str__(self):
        return f'{self.branch_office.name} {self.worker}'

    class Meta:
        verbose_name = 'Отчет о зарплате'
        verbose_name_plural = 'Отчеты о зарплате'


class Operation(models.Model):
    seller = models.ForeignKey(
        Employee, related_name='operation', on_delete=models.SET_NULL, null=True, verbose_name='Продавец'
    )
    shop: Shop = models.ForeignKey(Shop, related_name='operation', on_delete=models.CASCADE)
    branch_office: BranchOffice = models.ForeignKey(BranchOffice, related_name='operation', on_delete=models.CASCADE)
    cash_session: CashSession = models.ForeignKey(
        CashSession, related_name='operation', null=True, on_delete=models.SET_NULL
    )
    sum_product = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма продуктов')
    net_profit = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Чистая прибыль',
                                     null=True, blank=True)
    money_received = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Денег получено')
    change = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сдача')
    date_issue = models.DateTimeField(auto_now_add=True, verbose_name='Дата выдачи')
    operation_type = models.CharField(max_length=32, verbose_name='Способ оплаты')

    def __str__(self):
        return f"Operation {self.pk}.{self.sum_product}"

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'


class ProductOperation(models.Model):
    operation = models.ForeignKey(Operation, related_name='products', on_delete=models.CASCADE, verbose_name='Чек')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Продукт')
    name = models.CharField(max_length=64, verbose_name='Название')
    price = models.PositiveIntegerField(verbose_name='Цена упаковок', blank=True, default=0)
    piece_price = models.PositiveIntegerField(verbose_name='Цена штук', blank=True, default=0)
    quantity_package = models.PositiveIntegerField(verbose_name='Количество упаковок')
    quantity_piece = models.PositiveIntegerField(verbose_name='Количество штук')
    sum = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма')
    profit = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Прибыль', blank=True, null=True)
    barcode = models.PositiveBigIntegerField(verbose_name='Штрих код')

    def __str__(self):
        return f'Продукт {self.name}'

    class Meta:
        verbose_name = 'История продуктов для операции'
