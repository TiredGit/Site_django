from django.contrib import admin
from django.urls import path
from site_app import views

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()
router.register('users', views.MyUserAPI, basename='users')
router.register('categories', views.CategoryAPI, basename='categories')
router.register('services', views.ServiceAPI, basename='services')
router.register('masters', views.MasterAPI, basename='masters')
router.register('reviews', views.ReviewAPI, basename='reviews')
router.register('schedules', views.ScheduleAPI, basename='schedules')
router.register('record', views.RecordAPI, basename='records')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('main/', views.MainView.as_view(), name='main'),
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
    path('gallery_navigation/', views.gallery_navigation, name='gallery_navigation'),
    path('profile/<int:pk>/review/', views.ReviewView.as_view(), name='review'),
    path('profile/review/<int:pk>/delete/', views.DeleteReviewView.as_view(), name='review_delete'),
    path('profile/review/<int:pk>/update/', views.UpdateReviewView.as_view(), name='review_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)