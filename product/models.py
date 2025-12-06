from django.db import models
from django.utils import timezone

from account.models import Employee
from config.choices import CurrencyChoices, MeasurementChoices
from shop.models import BranchOffice, Shop


class ProductCategory(models.Model):
    shop = models.ForeignKey(Shop, related_name='product_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name='Название')
    image = models.ImageField(upload_to='product_category/%Y/%m/%d', default='default/product-image.jpg',
                              verbose_name='Фото категории продукта')

    def __str__(self):
        return f'{self.shop} - {self.name}'

    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'


class Provider(models.Model):
    shop = models.ForeignKey(Shop, related_name='provider', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name='Название')

    def __str__(self):
        return f'Поставщик {self.name}'

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Product(models.Model):
    branch_office: BranchOffice = models.ForeignKey(
        BranchOffice, related_name='product', on_delete=models.CASCADE, verbose_name='Филиал'
    )
    category: ProductCategory = models.ForeignKey(
        ProductCategory, related_name='product', on_delete=models.SET_NULL, null=True, verbose_name='Категория'
    )
    provider: Provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, verbose_name='Поставщик')
    name = models.CharField(max_length=64, verbose_name='Название товара')
    image = models.ImageField(upload_to='product/%Y/%m/%d', default='default/product-image.jpg',
                              verbose_name='Фото продукта')
    dimension = models.CharField(
        max_length=64, choices=MeasurementChoices.choices, default=MeasurementChoices.PIECE, verbose_name='Мерка'
    )
    cost_price = models.PositiveIntegerField(verbose_name='Себестоимость')
    income_percent = models.PositiveSmallIntegerField(verbose_name='Доход в процентах(%)')
    discount = models.PositiveSmallIntegerField(verbose_name='Скидка(%)', default=0)
    currency = models.CharField(max_length=16, choices=CurrencyChoices.choices,
                                default=CurrencyChoices.COM, verbose_name='Валюта')
    profit = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Чистая прибыль', null=True, blank=True)
    number_packages = models.IntegerField(verbose_name='Количство упаковок')
    piece_quantity = models.PositiveSmallIntegerField(verbose_name='Количство штук(осталось)', default=0)
    piece_in_package = models.PositiveSmallIntegerField(verbose_name='Количство штук в упаковке', default=0)
    received = models.PositiveIntegerField(verbose_name='Поступило')
    barcode = models.PositiveBigIntegerField(verbose_name='Штрих код')
    article_number = models.IntegerField(verbose_name='Артикул', default=0, blank=True, null=True)

    analogues = models.ManyToManyField('Product', blank=True, verbose_name='Аналоги')
    update_date_quantity = models.DateField(default=timezone.now())

    def __str__(self):
        return f"{self.name}"

    @property
    def piece_price(self) -> float:
        """ Цена за штуку """
        if not self.piece_in_package:
            return 0
        price_for_piece = self.price / self.piece_in_package
        return round(price_for_piece, 2)

    @property
    def price(self) -> float:
        """ Цена со скидкой """
        price = self.price_without_discount - self.discount_sum
        return round(price, 2)

    @property
    def discount_sum(self) -> float:
        """ Скидка  """
        discount_price = (self.price_without_discount / 100) * self.discount
        return discount_price

    @property
    def price_without_discount(self) -> float:
        """ Цена без скидки """
        without_discount = self.cost_price + self.cost_price / 100 * self.income_percent
        return without_discount

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Список продуктов'


class ProductInquiry(models.Model):
    branch_office = models.ForeignKey(BranchOffice, related_name='product_inquiry', on_delete=models.CASCADE)
    cashier = models.ForeignKey(Employee, related_name='product_inquiry', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveSmallIntegerField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Product inquiry - {self.cashier.first_name}'

    class Meta:
        verbose_name = 'Запрос на товар'
        verbose_name_plural = 'Запросы на товары'
