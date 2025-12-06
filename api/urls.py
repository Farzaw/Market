from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework_simplejwt.views import TokenRefreshView

from api.views import LoginApiView, ProductListApiView, ProductSearchApiView, CashSessionFinishApiView, \
    CashSessionStartApiView, OperationCreateApiView, UserInfoApiView, CashSessionInfoApiView, \
    CategoryListApiView, ProductInquiryCreateApiView, ProductAnalogueGetApiView, CategorySearchPApiView

app_name = 'api'


urlpatterns = [
    path('token/', LoginApiView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('cash-session/start/', CashSessionStartApiView.as_view(), name='cash_session_start'),
    path('cash-session/finish/', CashSessionFinishApiView.as_view(), name='cash_session_end'),
    path('cash-session/info/', CashSessionInfoApiView.as_view(), name='cash_session_info'),

    path('user/info/', UserInfoApiView.as_view(), name='user_info'),

    path('operation/create/', OperationCreateApiView.as_view(), name='operation_create'),

    path('product/inquiry/create/', ProductInquiryCreateApiView.as_view(), name='product_inquiry_create'),
    path('product/list/analogue/<int:product_id>/', ProductAnalogueGetApiView.as_view(), name='product_analogue_get'),
    path('product/list/', ProductListApiView.as_view(), name='product_list'),
    path('product/search/', ProductSearchApiView.as_view(), name='product_search'),

    path('category/list/', CategoryListApiView.as_view(), name='category_list'),
    path('category/<int:id>/search/product/', CategorySearchPApiView.as_view(), name='category_search_product'),

    path('download/documentation/', SpectacularAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
    path('', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
]
