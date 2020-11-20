from django.urls import path, include
from django.conf.urls import url
from apps.empresa.views import create_empresa, get_business, get_all_business

urlpatterns = [
    url('^create$', create_empresa),
    url('^retrieve$', get_all_business), 
    path('<str:business_id>', get_business),
    path('<str:business_id>/project/', include('apps.proyecto.urls')),
]