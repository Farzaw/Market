from django import forms

from account.models import Employee, Position, User
from config.choices import RoleChoices


class PositionChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return str(obj.name)


class EmployeeCreateForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=False)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Подтверждения пароля', required=False)
    position_id = PositionChoiceField(queryset=Position.objects.none(), empty_label=None, label='Должность')

    def __init__(self, shop_id, branch_office_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position_id'].queryset = Position.objects.filter(shop_id=shop_id)
        self.branch_office_id = branch_office_id
        self.shop_id = shop_id

    class Meta:
        model = Employee
        fields = (
            'first_name', 'last_name', 'position_id', 'address',
            'salary', 'currency', 'phone', 'email', 'password', 'password_confirm'
        )

    def save(self, commit=True):
        instance = super(EmployeeCreateForm, self).save(commit=False)
        instance.branch_office_id = self.branch_office_id
        instance.shop_id = self.shop_id

        if self.cleaned_data['email'] and self.cleaned_data['password']:
            user = User.objects.create_user(self.cleaned_data['email'], self.cleaned_data['password'])
            user.role = RoleChoices.CASHIER
            user.save()
            instance.user = user
        
        instance.save()
        return instance

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if not password and not password_confirm:
            return None

        if password_confirm != password:
            self.add_error('password_confirm', 'Пароли должны совпадать!')
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            return None

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Такой пользователь уже существует!')
        return email


class EmployeeUpdateForm(forms.ModelForm):
    position_id = PositionChoiceField(queryset=Position.objects.all(), label='Должность')

    def __init__(self, shop_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position_id'].queryset = Position.objects.filter(shop_id=shop_id)

    class Meta:
        model = Employee
        fields = (
            'position_id', 'first_name',
            'last_name', 'address', 'salary', 'currency', 'phone'
        )
