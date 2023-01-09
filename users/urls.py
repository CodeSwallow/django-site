from django.urls import path
from django.views.generic import TemplateView

from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('success/', TemplateView.as_view(template_name='users/success_registration.html'), name='success'),
]