# common/validators.py

from datetime import date
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication


def check_user_age_for_product_creation(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise PermissionDenied("Токен отсутствует или некорректен")

    raw_token = auth_header.split(' ')[1]

    try:
        validated_token = JWTAuthentication().get_validated_token(raw_token)
        birthdate_str = validated_token.get('birthdate')

        if birthdate_str is None:
            raise ValidationError(
                detail="Укажите дату рождения, чтобы создать продукт.",
                code='birthdate_required'
            )

        birth_date = date.fromisoformat(birthdate_str)

        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if age < 18:
            raise PermissionDenied("Вам должно быть 18 лет, чтобы создать продукт.")

    except ValueError:
        raise ValidationError("Некорректный формат даты рождения в токене.")
    except Exception as e:
        raise PermissionDenied(f"Ошибка проверки токена: {str(e)}")