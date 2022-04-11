from django.core.exceptions import ValidationError


def validate_phone(phone):
    if not phone.isdigit():
        raise ValidationError('Номер должен состоять из цифр')
    if len(phone) != 9:
        raise ValidationError('Неверный ввод номера')
    return phone
