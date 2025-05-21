from django.urls import path, include

urlpatterns = [
    path('', include('sops.urls')),
]
