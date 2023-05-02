"""
URL configuration for apotheker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('drugs', views.list_drugs, name='list_drugs'),
    path('receipts', views.list_receipts, name='list_receipts'),
    path('add-drug', views.add_drug, name='add_drug'),
    path('delete-drug/<drug_id>', views.delete_drug, name='delete_drug'),
    path('add-receipt', views.add_receipt, name='add_receipt'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
]
