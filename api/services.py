from rest_framework.exceptions import NotFound

from account.models import CashSession, Employee


def get_active_cash_session(employee: Employee) -> CashSession:
    cash_sessions = employee.cash_session.filter(is_active=True)
    if not cash_sessions.exists():
        raise NotFound(detail='Сash session has not been created')
    return cash_sessions.last()


def count_number_pieces(product, front_package, front_piece):
    p_piece_max = product.piece_in_package
    if not p_piece_max:
        product.number_packages -= front_package
        product.save()
        return product

    # Считаем сколько состовляет упаковок из штук
    left_package_from_piece = front_piece // p_piece_max
    front_package += left_package_from_piece

    # Штук осталось
    front_piece_left = front_piece % p_piece_max

    if product.piece_quantity < front_piece_left:
        product.number_packages -= 1
        product.piece_quantity += p_piece_max

    product.piece_quantity -= front_piece_left
    product.number_packages -= front_package

    product.save()
    return product
