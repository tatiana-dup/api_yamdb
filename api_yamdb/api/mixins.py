from rest_framework.exceptions import ValidationError


class UsernameValidatorMixin:
    """Миксин для валидации username."""
    def validate_username(self, value):
        if value.lower() == "me":
            raise ValidationError(
                "Вы не можете выбрать юзернейм 'me', "
                "выберите другой юзернейм.")
        return value
