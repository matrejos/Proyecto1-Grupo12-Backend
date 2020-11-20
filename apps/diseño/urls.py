from django.urls import path
from django.conf.urls import include, url
from apps.diseño.views import design_list, design_detail

urlpatterns = [       
    url('^$', design_list),    
    path('<uuid:design_pk>', design_detail), 
]