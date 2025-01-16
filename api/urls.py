from authentication import views as authetication_views
from users import views as user_views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('register/', authetication_views.register_user, name='register_user'),
    path('token/', authetication_views.login_user, name='login_user'),
    path('logout/', authetication_views.logout, name='logout_user'),
    path('token/refresh/', authetication_views.generate_new_access_token, name='refresh_token'),
    path('profile/', user_views.user_profile, name='user_profile'),

    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

'''
## Endpoints
- `POST /api/register/` - Register a new user
- `POST /api/token/` - Login to get JWT
- `POST /api/token/blacklist/` - Blacklist a token
- `GET/POST /api/profile/` - Manage user profile

- `POST /api/forgot-password/` - Mock password reset
- `POST /api/change-password/` - Change password

email
password
refresh_token


'''