from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='home'),

    path('vid/<int:id>/', vidView, name='vid-view'),
    path('vid-upload/', vidUpload, name='vid-upload'),
    path('dyna/', dyna, name='dyna'),

]