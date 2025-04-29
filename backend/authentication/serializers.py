from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Позволяет вводить в поле 'username' либо сам username, либо email.
    """
    def validate(self, attrs):
        login = attrs.get(self.username_field)
        password = attrs.get("password")

        # если ввели email или username — найдем пользователя
        try:
            user = User.objects.get(Q(username__iexact=login) | Q(email__iexact=login))
            attrs[self.username_field] = user.username
        except User.DoesNotExist:
            # дальше отработает оригинальный валидатор и выбросит ошибку
            pass

        data = super().validate(attrs)

        # добавим в ответ пару полей про пользователя
        data.update({
            "user_id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        })
        return data
