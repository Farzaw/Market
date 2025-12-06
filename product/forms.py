from django import forms

from product.models import Product, ProductCategory, BranchOffice, Provider


class ProductCategoryChoices(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return str(obj.name)


class ProductAnaloguesChoicesField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return str(obj.name)


class ProductCreateForm(forms.ModelForm):
    category = ProductCategoryChoices(queryset=ProductCategory.objects.none(), label='Категория')
    analogues = ProductAnaloguesChoicesField(queryset=Product.objects.none(), label='Аналог', required=False)

    def __init__(self, shop_id, *args, **kwargs):
        self.branch_office_id = kwargs.pop('branch_office_id')
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = ProductCategory.objects.filter(shop_id=shop_id)
        self.fields['analogues'].queryset = Product.objects.filter(branch_office=self.branch_office_id)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'provider', 'dimension', 'cost_price', 'income_percent', 'discount', 'currency',
            'received', 'piece_in_package', 'barcode', 'article_number', 'image', 'analogues'
        )

    def clean_barcode(self):
        barcode = self.cleaned_data['barcode']
        if BranchOffice.objects.filter(id=self.branch_office_id, product__barcode=barcode).exists():
            self.add_error('barcode', 'Такой штрих код уже есть')
        return barcode

    def save(self, commit=True):
        instance = super(ProductCreateForm, self).save(commit=False)
        instance.branch_office_id = self.branch_office_id
        instance.number_packages = instance.received
        instance.profit = self.cleaned_data['cost_price'] / 100 * self.cleaned_data['income_percent']
        instance.save()
        return instance


class ProductUpdateForm(forms.ModelForm):
    category = ProductCategoryChoices(queryset=ProductCategory.objects.none())
    analogues = ProductAnaloguesChoicesField(queryset=Product.objects.none(), required=False)
    
    def save(self, commit=True):
        cd = self.cleaned_data
        self.instance.profit = cd['cost_price'] / 100 * cd['income_percent']
        self.instance.save()
        return super().save(commit)

    def __init__(self, shop_id, branch_office, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ProductCategory.objects.filter(shop_id=shop_id)
        self.fields['analogues'].queryset = Product.objects.filter(branch_office=branch_office)

    class Meta:
        model = Product
        fields = (
            'name', 'category', 'provider', 'cost_price', 'dimension', 'income_percent', 'discount', 'currency',
            'number_packages', 'piece_in_package', 'barcode', 'article_number', 'image', 'analogues'
        )


class CategoryProductCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.shop_id = kwargs.pop('shop_id')
        super(CategoryProductCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = ProductCategory.objects.create(
            name=self.cleaned_data.get('name'),
            shop_id=self.shop_id
        )
        return instance

    class Meta:
        model = ProductCategory
        fields = ('name',)


class ProviderCreateForm(forms.ModelForm):
    
    def __init__(self, shop_id, *args, **kwargs):
        self.shop_id = shop_id
        super(ProviderCreateForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        self.instance = Provider.objects.create(
            shop_id=self.shop_id,
            name=self.cleaned_data['name'])
        return self.instance

    class Meta:
        model = Provider
        fields = ('name',)


class ProviderUpdateForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = ('name',)
