from django.urls import path

# import views here
from .views import home_page

urlpatterns = [
    path('', home_page, name='home-page'),
]