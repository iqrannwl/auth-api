from django.contrib import admin
from django.urls import path, include


api_path_group = [
    path("accounts/", include("accounts.urls"))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("v1/api/", include(api_path_group))
]
