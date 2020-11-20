from django.urls import path
from django.conf.urls import include, url
from apps.proyecto.views import project_list, project_detail

urlpatterns = [    
    url('^$', project_list),
    path('<uuid:proyecto_pk>', project_detail),    
    path('<uuid:proyecto_pk>/design/', include('apps.diseño.urls')),
]