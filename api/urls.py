from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register('admin/advisor', views.AdvisorView)

urlpatterns = [
    path('', include(router.urls)),
    path('user/register/', views.register),
    path('user/login/', views.login),
    path('user/<int:user_id>/advisor/', views.advisor_list),
    path('user/<int:user_id>/advisor/<int:advisor_id>/', views.book_advisor),
    path('user/<int:user_id>/advisor/booking/', views.get_bookings),
]
