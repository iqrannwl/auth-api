from django.urls import path
from .views import SignupView, LoginView, UserProfile, UpdateUserProfile, ChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView

urlpatterns = [
    path("singup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", UserProfile.as_view(), name="profile"),
    path("profile/update/", UpdateUserProfile.as_view(), name="update_profile"),
    path("changepassword/", ChangePasswordView.as_view(), name="change_password"),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]
