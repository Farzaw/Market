from django.contrib import auth
from django.utils import timezone
from django.db.models import Sum
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from account.models import User, CashSession, Employee
from api.services import get_active_cash_session, count_number_pieces
from product.models import Product, ProductCategory, ProductInquiry
from report.models import Operation, ProductOperation


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, data) -> str:
        user = User.objects.get(email=data['email'])
        return user.get_token()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid email or password')
        if not user.is_active:
            raise AuthenticationFailed('Account is not active')
        if not user.is_cashier():
            raise AuthenticationFailed("You don't have access")
        return attrs

    class Meta:
        model = User
        fields = ('email', 'password', 'token')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'phone')


class UserInfoSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'employee')


class CashSessionStartSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        self.validated_data['cashier'] = self.employee
        return super().save(**kwargs)

    def validate(self, attrs):
        self.employee = self.context['request'].user.employee
        if self.employee.cash_session.filter(is_active=True).exists():
            raise ValidationError(detail='User already has an active cash session')
        return attrs

    class Meta:
        model = CashSession
        fields = ('id', 'cashier', 'start_time', 'money_start', 'is_active')
        read_only_fields = ('id', 'cashier', 'start_time', 'is_active')


class CashSessionFinishSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        validated_data['end_time'] = timezone.now()
        validated_data['is_active'] = False
        return super().update(instance, validated_data)

    class Meta:
        model = CashSession
        fields = ('id', 'cashier', 'start_time', 'end_time', 'money_start', 'money_end', 'is_active')
        read_only_fields = ('id', 'cashier', 'start_time', 'end_time', 'money_start', 'is_active')


class CashSessionInfoSerializer(serializers.ModelSerializer):
    money_collected = serializers.SerializerMethodField()

    def get_money_collected(self, cash_session) -> float:
        money_collected = cash_session.operation.aggregate(product_sum=Sum('sum_product'))
        return money_collected['product_sum']

    class Meta:
        model = CashSession
        fields = ('start_time', 'money_start', 'money_collected', 'is_active')


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    analogues_count = serializers.SerializerMethodField(method_name='get_analogues_count')

    def get_analogues_count(self, instance) -> int:
        return instance.analogues.all().count()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'number_packages', 'piece_quantity', 'piece_in_package', 'dimension',
            'price_without_discount', 'discount', 'discount_sum', 'price', 'piece_price', 'barcode', 'category',
            'image', 'analogues_count'
        )


class ProductInquiryCreateSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        employee = self.context['request'].user.employee
        self.validated_data['cashier'] = employee
        self.validated_data['branch_office'] = employee.branch_office
        return super().save()

    class Meta:
        model = ProductInquiry
        fields = ('id', 'product', 'quantity')


class ProductAnalogueGetSerializer(serializers.ModelSerializer):
    analogues = ProductSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'analogues')


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'image')


class ProductOperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOperation
        exclude = ('id', 'operation', 'profit')


class OperationCreateSerializer(WritableNestedModelSerializer):
    products = ProductOperationSerializer(many=True)

    def create(self, validated_data):
        """ Сократить количесто запросов *** """
        employee = self.context['request'].user.employee
        operation = Operation.objects.create(
            seller=employee,
            shop=employee.branch_office.shop,
            branch_office=employee.branch_office,
            cash_session=get_active_cash_session(employee),
            sum_product=validated_data['sum_product'],
            money_received=validated_data['money_received'],
            change=validated_data['change'],
            operation_type=validated_data['operation_type']
        )

        net_profit = 0
        for product_operation in validated_data['products']:
            product = product_operation['product']
            net_profit += product.profit
            ProductOperation.objects.create(
                operation=operation,
                product=product,
                name=product_operation['name'],
                price=product_operation['price'],
                piece_price=product_operation['piece_price'],
                quantity_package=product_operation['quantity_package'],
                quantity_piece=product_operation['quantity_piece'],
                sum=product_operation['sum'],
                profit=product.profit,
                barcode=product_operation['barcode']
            )
            count_number_pieces(product, product_operation['quantity_package'], product_operation['quantity_piece'])
        operation.net_profit = net_profit
        operation.save()
        return operation

    class Meta:
        model = Operation
        fields = (
            'id', 'products', 'sum_product', 'money_received', 'change', 'date_issue', 'operation_type'
        )
