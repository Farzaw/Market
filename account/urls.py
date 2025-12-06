from django.urls import path

from account.views import LoginView, LogoutView, EmployeeListView, EmployeeCreateView, EmployeeUpdateView, \
    EmployeeDeleteView, BranchEmployeeList


app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('employee/list/', EmployeeListView.as_view(), name='employee_list'),
    path('employee/create/<int:branch_id>/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),

    path('employee/branch/<int:branch_id>/list/', BranchEmployeeList.as_view(), name='branch_employee_list'),
]
