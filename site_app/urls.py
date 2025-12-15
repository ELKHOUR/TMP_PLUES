from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import confirm_email

urlpatterns = [
    path('', views.index, name='home'),
    path('application_form/', views.application_form, name='application_form'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('product/<int:pk>/', views.ProductView.as_view(), name='product'),
    path('confirm-email/<uuid:token>/', views.confirm_email, name='confirm_email'),
    path('contact/', views.contact, name='contact'),

]