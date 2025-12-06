from django import forms

from config.choices import RoleChoices
from shop.models import BranchOffice, Position, PhotoDocument
from account.models import User


class BranchCreateForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Подтверждения пароль')

    def __init__(self, request, *args, **kwargs):
        super(BranchCreateForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password_confirm != password:
            self.add_error('password_confirm', 'Пароли должны совпадать!')
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Такой пользователь уже существует!')
        return email

    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = User.objects.create_user(password=password, email=email)
        user.role = RoleChoices.BRANCH_ADMIN
        user.save()
        branch = super().save(commit=False)
        branch.owner = user
        branch.shop = self.request.user.shop
        branch.save()
        return super(BranchCreateForm, self).save(commit)

    class Meta:
        model = BranchOffice
        fields = ('id', 'name', 'address', 'phone', 'country', 'city', 'email', 'password', 'password_confirm')


class BranchUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False, initial='')
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Поменять пароль')
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=False, label='Подтвердить пароль')

    def __init__(self, *args, **kwargs):
        self.view = kwargs.pop('view')
        super().__init__(*args, **kwargs)
        self.fields.get('email').initial = self.instance.owner.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() and self.instance.owner.email != email:
            self.add_error('email', 'Такой пользователь уже существует!')
        return email

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm != password:
            self.add_error('password_confirm', 'Пароли должны совпадать!')
        return password

    def save(self, commit=True):
        data = self.cleaned_data
        email = data.pop('email')
        password = data.pop('password')
        instance = super().save()

        instance.owner.email = email
        if password:
            instance.owner.set_password(password)
        instance.owner.save()
        instance.save()
        return instance

    class Meta:
        model = BranchOffice
        fields = ('id', 'name', 'address', 'phone', 'country', 'city', 'email', 'password', 'password_confirm')


class PositionCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.shop = kwargs.pop('shop')
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = Position.objects.create(name=self.cleaned_data.get('name'), shop=self.shop)
        return instance

    class Meta:
        model = Position
        fields = ('name',)
