from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', views.admin_page, name='admin_page'),
    path('delete/<int:sop_id>/', views.delete_sop, name='delete_sop'),
    path('update/<int:sop_id>/', views.update_sop, name='update_sop'),
]
