from django.urls import path
from . import views

urlpatterns = [
    # Admin interface URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', views.admin_page, name='admin_page'),
    path('delete/<int:sop_id>/', views.delete_sop, name='delete_sop'),
    path('update/<int:sop_id>/', views.update_sop, name='update_sop'),
    
    # API endpoints
    path('api/sops/', views.api_sops, name='api_sops'),
    path('api/sops/<int:sop_id>/', views.api_sop_detail, name='api_sop_detail'),
]