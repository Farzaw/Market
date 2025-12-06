from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Список категорий'


class Shop(models.Model):
    owner = models.OneToOneField('account.User', related_name='shop', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='shop', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=16)
    itn = models.IntegerField()
    okpo = models.CharField(max_length=128)
    registration_justice = models.DateField()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Список магазинов'


class PhotoDocument(models.Model):
    shop = models.ForeignKey(Shop, related_name='photo_document', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name='Название')
    image = models.ImageField(upload_to='documents/%Y/%m/%d', verbose_name='Фото документа')

    def __str__(self):
        return str(self.shop)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Список документов'


class Position(models.Model):
    shop = models.ForeignKey(Shop, related_name='position', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, verbose_name='Должность')

    def __str__(self):
        return str(self.shop) + "->" + str(self.name)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Список должностей'


class BranchOffice(models.Model):
    owner = models.OneToOneField('account.User', related_name='branch_office', null=True, on_delete=models.SET_NULL)
    shop = models.ForeignKey(Shop, related_name='branch_office', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name='Название филиала')
    address = models.CharField(max_length=256, verbose_name='Адрес')
    phone = models.CharField(max_length=16, verbose_name='Номер телефона')
    country = models.CharField(max_length=32, verbose_name='Страна')
    city = models.CharField(max_length=32, verbose_name='Город')

    def __str__(self):
        return str(self.shop) + "->" + str(self.owner)

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Список филиалов'
