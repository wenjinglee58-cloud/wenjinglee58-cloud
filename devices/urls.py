from django.urls import path
from . import views

urlpatterns = [
    path('toggle-background-refresh/<int:device_id>/', views.toggle_background_refresh, name='toggle_background_refresh'),
    path('bulk-toggle-background-refresh/', views.bulk_toggle_background_refresh, name='bulk_toggle_background_refresh'),
    path('background-refresh-management/', views.background_refresh_management, name='background_refresh_management'),
    path('toggle-background-activity/<int:device_id>/', views.toggle_background_activity, name='toggle_background_activity'),
    path('background-activity-management/', views.background_activity_management, name='background_activity_management'),
    path('generate-mdm-profile/', views.generate_mdm_profile, name='generate_mdm_profile'),
]