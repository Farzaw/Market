from django.urls import path

from shop.views import (
    IndexView, BranchListView, BranchCreateView, BranchUpdateView, BranchDeleteView, BranchDetailView, PositionListView,
    PositionCreateView, PositionDeleteView
)


app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('branch-list/', BranchListView.as_view(), name='branch_list'),
    path('branch-create/', BranchCreateView.as_view(), name='branch_create'),
    path('branch-detail/<int:branch_id>/', BranchDetailView.as_view(), name='branch_detail'),
    path('branch-update/<int:branch_id>/', BranchUpdateView.as_view(), name='branch_update'),
    path('branch-delete/<int:branch_id>/', BranchDeleteView.as_view(), name='branch_delete'),

    path('position/list/', PositionListView.as_view(), name='position_list'),
    path('position/create/', PositionCreateView.as_view(), name='position_create'),
    path('position/delete/<int:pk>/', PositionDeleteView.as_view(), name='position_delete'),
]
