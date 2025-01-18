from authentication import views as authetication_views
from user_details import views as user_profile_views

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
    path('forget_password/',  authetication_views.forget_password, name = 'forget_password'),
    path('new_password_otp/', authetication_views.new_password_otp, name = 'change_password_otp'),
    path('change_password/',  authetication_views.change_password, name = 'change_password'),

    path('get_profile/', user_profile_views.get_user_profile, name='get_user_profile'),
    path('create_profile/', user_profile_views.create_user_profile, name='create_user_profile'),
    path('update_profile/', user_profile_views.update_user_profile, name='update_user_profile'),
    path('delete_profile/', user_profile_views.delete_user_profile, name='delete_user_profile'),

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