from django.urls import path
from . import views

urlpatterns = [
    path('scrape/', views.scrape_playstore, name='scrape_playstore'),
    path('package/<str:package_name>/', views.get_package_details, name='get_package_details'),
    path('packages/', views.get_all_packages, name='get_all_packages'),
]
