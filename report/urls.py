from django.urls import path

from report.views import SalaryReportListView, SalaryReportCreateView, SalaryReportDeleteView, \
    OperationListView

app_name = 'report'

urlpatterns = [
    path('salary-report/list/', SalaryReportListView.as_view(), name='salary_report_list'),
    path('salary-report/create/', SalaryReportCreateView.as_view(), name='salary_report_create'),
    path('salary-report/<int:pk>/delete/', SalaryReportDeleteView.as_view(), name='salary_report_delete'),

    path('operation-report/list/', OperationListView.as_view(), name='operation_report_list'),
]
