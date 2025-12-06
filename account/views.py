from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView as Logout
from django.contrib import messages
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from account.forms import EmployeeCreateForm, EmployeeUpdateForm
from account.filters import EmployeeFilter
from account.models import Employee
from shop.models import BranchOffice
from shop.permissions import IsAdminRolePermission, ShopAdminPermission


""" Authentication """


class LoginView(TemplateView):
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_role_admin():
                login(request, user)
                messages.success(request=request, message=f"Вы вошли в систему как {user.email}.")
                return redirect('shop:index')
            else:
                form.add_error(field=None, error='У вас не достаточно прав!')
                return render(request, self.template_name, context={'form': form})
        return render(request, self.template_name, context={'form': form})


class LogoutView(Logout):
    pass


""" Employee CRUD """


class EmployeeListView(ShopAdminPermission, ListView):
    template_name = 'account/pages/employee_list.html'
    model = Employee

    def get_queryset(self):
        return self.request.user.shop.branch_office.all()


class EmployeeCreateView(IsAdminRolePermission, CreateView):
    template_name = 'account/forms/employee_create.html'
    model = Employee
    form_class = EmployeeCreateForm

    def get_form_kwargs(self):
        form_kwargs = super(EmployeeCreateView, self).get_form_kwargs()
        form_kwargs['shop_id'] = BranchOffice.objects.get(id=self.kwargs.get('branch_id')).shop.id
        form_kwargs['branch_office_id'] = self.kwargs.get('branch_id')
        return form_kwargs

    def get_success_url(self):
        return reverse('account:branch_employee_list', kwargs={'branch_id': self.kwargs.get('branch_id')})


class EmployeeUpdateView(IsAdminRolePermission, UpdateView):
    template_name = 'account/forms/employee_update.html'
    model = Employee
    form_class = EmployeeUpdateForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['shop_id'] = self.get_object().branch_office.shop.id
        return form_kwargs

    def get_success_url(self):
        return reverse('account:branch_employee_list', kwargs={'branch_id': self.get_object().branch_office.id})


class EmployeeDeleteView(IsAdminRolePermission, DeleteView):
    template_name = 'account/forms/employee_delete.html'
    model = Employee

    def get_success_url(self):
        messages.success(self.request, 'Успешно удалено!')
        success_url = reverse('account:branch_employee_list', kwargs={'branch_id': self.kwargs.get('branch_id')})
        return success_url

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.kwargs['branch_id'] = self.object.branch_office.id
        self.object.delete()
        if self.object.user:
            self.object.user.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


""" Branch Employee list  """


class BranchEmployeeList(IsAdminRolePermission, ListView):
    template_name = 'account/pages/branch_employee_list.html'
    paginate_by = 10
    model = Employee

    def get(self, request, *args, **kwargs):
        form = EmployeeFilter(request.GET, queryset=self.get_queryset(), request=request)
        self.object_list = form.qs
        context = self.get_context_data(form=form, branch_id=self.kwargs.get('branch_id'))
        return self.render_to_response(context)

    def get_queryset(self):
        return self.model.objects.filter(branch_office=self.kwargs.get('branch_id')).order_by('-id')
