"""
URL configuration for site_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from site_app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainView.as_view(), name='main'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('booking/service', views.BookingServiceView.as_view(), name='booking_service'),
    path('booking/save_service/<int:service_id>/', views.save_selected_service, name='save_selected_service'),
    path('booking/master', views.BookingMasterView.as_view(), name='booking_master'),
    path('booking/save_master/<int:master_id>/', views.save_selected_master, name='save_selected_master'),
    path('booking/date', views.BookingDateView.as_view(), name='booking_date'),
    path('booking/save_schedule/<int:schedule_id>/', views.save_selected_schedule, name='save_selected_schedule'),
    path('booking/create_record', views.create_record, name='create_record'),
    path('profile/cancel_record/<int:pk>/', views.RecordDeleteView.as_view(), name='cancel_record'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('gallery/', views.gallery, name='gallery'),
    path('profile/<int:pk>/review/', views.ReviewView.as_view(), name='review'),
    path('profile/review/<int:pk>/delete/', views.DeleteReviewView.as_view(), name='review_delete'),
    path('profile/review/<int:pk>/update/', views.UpdateReviewView.as_view(), name='review_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)