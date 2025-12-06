from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import BranchOffice, Position, Shop
from config.choices import RoleChoices, CurrencyChoices


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if password is None:
            raise TypeError(_('Password should be not none'))
        if email is None:
            raise TypeError(_('Users should be an Email'))
        user: User = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user: User = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=128, unique=True)
    role = models.CharField(max_length=12, choices=RoleChoices.choices, verbose_name=_('Role'))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    def is_role_admin(self):
        return self.role in {
            RoleChoices.SHOP_ADMIN,
            RoleChoices.BRANCH_ADMIN
        }

    def is_shop_admin(self):
        return True if self.role == RoleChoices.SHOP_ADMIN else False

    def is_branch_admin(self):
        return True if self.role == RoleChoices.BRANCH_ADMIN else False

    def is_cashier(self):
        return True if self.role == RoleChoices.CASHIER else False

    def get_token(self) -> dict:
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Список пользователей'


class Employee(models.Model):
    user: User = models.OneToOneField(User, related_name='employee', null=True, blank=True, on_delete=models.CASCADE)
    position_id: Position = models.ForeignKey(Position, related_name='employee', null=True, on_delete=models.SET_NULL)
    shop: Shop = models.ForeignKey(Shop, related_name='employees', on_delete=models.CASCADE)
    branch_office: BranchOffice = models.ForeignKey(BranchOffice, related_name='employee', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, verbose_name='Имя')
    last_name = models.CharField(max_length=32, verbose_name='Фамилия')
    address = models.CharField(max_length=128, verbose_name='Адрес')
    phone = models.CharField(max_length=16, verbose_name='Номер телефона')
    salary = models.IntegerField(verbose_name='Зарплата')
    currency = models.CharField(max_length=16, choices=CurrencyChoices.choices, verbose_name='Валюта')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Список сотрудников'


class CashSession(models.Model):
    cashier = models.ForeignKey(
        Employee, blank=False, null=True, on_delete=models.SET_NULL, related_name='cash_session'
    )
    is_active = models.BooleanField(verbose_name='Работеат', default=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    money_start = models.DecimalField(max_digits=9, decimal_places=2)
    money_end = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'Session {self.pk} {self.cashier}'

    class Meta:
        verbose_name = 'Сессия кассы'
        verbose_name_plural = 'Сессии кассы'
