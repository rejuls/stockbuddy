from django.conf import settings
from django.urls import include, path
from . import views
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.stock_view, name='home'),
    path('stock/<str:symbol>', views.stockdetail_view, name='detailed'),
]
