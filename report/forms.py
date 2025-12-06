from django import forms

from report.models import SalaryReport
from account.models import Employee


class EmployeeChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.last_name} {obj.first_name}'


class SalaryReportCreateForm(forms.ModelForm):
    worker = EmployeeChoiceField(queryset=Employee.objects.none(), label='Работник')

    def __init__(self, shop_id, branch_id,  *args, **kwargs):
        super(SalaryReportCreateForm, self).__init__(*args, **kwargs)
        if branch_id:
            self.fields['worker'].queryset = Employee.objects.filter(branch_office_id=branch_id)
        elif shop_id:
            self.fields['worker'].queryset = Employee.objects.filter(branch_office__shop_id=shop_id)

    class Meta:
        model = SalaryReport
        fields = ('id', 'worker', 'got_money', 'currency', 'date_from', 'date_before')

    def save(self, commit=True):
        branch_office = self.cleaned_data.get('worker').branch_office
        self.cleaned_data['branch_office'] = branch_office
        self.cleaned_data['shop'] = branch_office.shop
        instance = self._meta.model.objects.create(**self.cleaned_data)
        return instance
