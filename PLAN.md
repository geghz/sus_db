# SUS_DB — Глобальный план реализации

---

# 1. Авторизация

## Frontend

- **Компонент** `LoginForm`  
  - Поля:  
    - «Логин или Email»  
    - «Пароль»  
    - «Запомнить меня» (чекбокс)  
  - Использовать библиотеки:  
    - `react-hook-form` + `@hookform/resolvers/yup` для валидации формы  
    - `yup` для описания схемы валидации  

- **Хранение токенов**  
  - `accessToken` — в React-контексте (`AuthContext`) или `localStorage`  
  - `refreshToken` — в httpOnly-cookie  

- **Авто-обновление токена**  
  - Перехватывать ответы с 401 в Axios  
  - При 401 и флаге `!_retry` → отправлять `POST /api/auth/token/refresh/`, сохранять новый `accessToken` и повторять оригинальный запрос

- **Редиректы**  
  - До входа: защищённые роуты перенаправляют на `/login`  
  - После успешного входа:  
    1. Если пользователь пытался зайти на защищённый адрес → вернуть его туда  
    2. Иначе → на `/` (Dashboard)

## Backend

- **DRF SimpleJWT**  
  - Кастомный сериализатор для логина по username или email:
    ```python
    class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
        def validate(self, attrs):
            login = attrs.get(self.username_field)
            # ищем пользователя по username или email (Q)
            # подставляем attrs['username'] = real_username
            data = super().validate(attrs)
            data.update({
                "user_id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
            })
            return data
    ```
  - Кастомный view:
    ```python
    class CustomTokenObtainPairView(TokenObtainPairView):
        serializer_class = CustomTokenObtainPairSerializer
    ```
- **URL-паттерны** в `authentication/urls.py`:
  ```python
  urlpatterns = [
      path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  ]
