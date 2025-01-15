from authentication import views
from django.urls import path
urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('token/', views.login_user, name='login_user'),
    path('profile/', views.user_profile, name='user_profile')
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