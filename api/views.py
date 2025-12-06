from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, filters, serializers
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from account.models import User, CashSession
from api.serializers import (
    LoginSerializer, ProductSerializer, CashSessionFinishSerializer, CashSessionStartSerializer,
    OperationCreateSerializer, UserInfoSerializer, CashSessionInfoSerializer, CategoryListSerializer,
    ProductInquiryCreateSerializer, ProductAnalogueGetSerializer
)
from api.permissions import IsCashierPermission
from api.services import get_active_cash_session
from product.models import Product, ProductCategory, ProductInquiry
from report.models import Operation


class LoginApiView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        responses=inline_serializer(
            name='Token',
            fields={
                'email': serializers.EmailField(),
                'token': inline_serializer(
                    name='Nested-Token',
                    fields={
                        'access': serializers.CharField(),
                        'refresh': serializers.CharField()
                    }
                )
            })
    )
    def post(self, request):
        """ Authentication """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserInfoApiView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [IsCashierPermission]

    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CashSessionStartApiView(CreateAPIView):
    queryset = CashSession.objects.all()
    serializer_class = CashSessionStartSerializer
    permission_classes = [IsCashierPermission]


class CashSessionFinishApiView(GenericAPIView, UpdateModelMixin):
    queryset = CashSession.objects.all()
    serializer_class = CashSessionFinishSerializer
    permission_classes = [IsCashierPermission]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        employee = self.request.user.employee
        instance = get_active_cash_session(employee)
        return instance


class CashSessionInfoApiView(GenericAPIView):
    queryset = CashSession
    serializer_class = CashSessionInfoSerializer
    permission_classes = [IsCashierPermission]

    def get(self, request):
        cash_session = self.get_object()
        serializer = self.get_serializer(cash_session)
        return Response(serializer.data)

    def get_object(self):
        return get_active_cash_session(self.request.user.employee)


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsCashierPermission]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.request.user.employee.branch_office.product.all()


class ProductSearchApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'barcode']
    permission_classes = [IsCashierPermission]

    def get_queryset(self):
        return self.request.user.employee.branch_office.product.all()


class ProductInquiryCreateApiView(CreateAPIView):
    queryset = ProductInquiry.objects.all()
    serializer_class = ProductInquiryCreateSerializer
    permission_classes = [IsCashierPermission]


class ProductAnalogueGetApiView(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAnalogueGetSerializer
    permission_classes = [IsCashierPermission]

    def get(self, request, **kwargs):
        serializer = self.get_serializer(self.get_object(), many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.request.user.employee.branch_office.product.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=self.kwargs['product_id'])


class CategoryListApiView(ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [IsCashierPermission]

    def get_queryset(self):
        return self.request.user.employee.shop.product_category.all()


class CategorySearchPApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsCashierPermission]

    def get_queryset(self):
        if self.kwargs['id'] == 0:
            return self.request.user.employee.branch_office.product.all()
        return self.request.user.employee.branch_office.product.filter(category_id=self.kwargs['id'])


class OperationCreateApiView(CreateAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationCreateSerializer
    permission_classes = [IsCashierPermission]

    # @extend_schema(responses={201: None})
    # def post(self, request, *args, **kwargs):
    """ не сопостовляет с продуктом и с продутом операции """
    #     data = request.data
    #     employee = request.user.employee
    #     operation = Operation(
    #         seller=employee,
    #         shop=employee.branch_office.shop,
    #         branch_office=employee.branch_office,
    #         cash_session=get_active_cash_session(employee),
    #         sum_product=data['sum_product'],
    #         money_received=data['money_received'],
    #         change=data['change'],
    #         operation_type=data['operation_type']
    #     )
    #
    #     net_profit = 0
    #     list_pr_operation = []
    #
    #     ids = [i['product'] for i in data['products']]
    #     products = Product.objects.filter(id__in=ids).all()
    #
    #     for product_operation, product in zip(data['products'], products):
    #         net_profit += product.profit
    #         pro = ProductOperation(
    #             operation=operation,
    #             product_id=product.id,
    #             name=product_operation['name'],
    #             price=product_operation['price'],
    #             piece_price=product_operation['piece_price'],
    #             quantity_package=product_operation['quantity_package'],
    #             quantity_piece=product_operation['quantity_piece'],
    #             sum=product_operation['sum'],
    #             profit=product.profit,
    #             barcode=product_operation['barcode']
    #         )
    #         list_pr_operation.append(pro)
    #         count_number_pieces(product, product_operation['quantity_package'], product_operation['quantity_piece'])
    #     operation.net_profit = net_profit
    #     operation.save(force_insert=True)
    #     ProductOperation.objects.bulk_create(list_pr_operation)
    #     return Response(status=status.HTTP_201_CREATED)