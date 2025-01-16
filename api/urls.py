from authentication import views as authetication_views
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
    
    # path('profile/', views.user_profile, name='user_profile')

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

'''
## Endpoints
- `POST /api/register/` - Register a new user
- `POST /api/token/` - Login to get JWT
- `POST /api/token/blacklist/` - Blacklist a token
- `POST /api/forgot-password/` - Mock password reset
- `POST /api/change-password/` - Change password
- `GET/POST /api/profile/` - Manage user profile

email
password
refresh_token


'''