from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.conf import settings

from account.models import User

""" Use this '<int:branch_id>/' in url if you are doing something with Model BranchOffice """


class IsAdminRolePermission(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_role_admin():
            return redirect(settings.LOGIN_URL)
        # Доделать
        try:
            if kwargs.get('branch_id') and \
                    not request.user.branch_office.shop.branch_office.filter(id=kwargs.get('branch_id')):
                return redirect('shop:index')
        except User.branch_office.RelatedObjectDoesNotExist as e:
            if kwargs.get('branch_id') and not request.user.shop.branch_office.filter(id=kwargs.get('branch_id')):
                return redirect('shop:index')
        return super().dispatch(request, *args, **kwargs)


class ShopAdminPermission(IsAdminRolePermission):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_shop_admin():
            return redirect('shop:index')
        return super().dispatch(request, *args, **kwargs)
