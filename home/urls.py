from django.urls import path
from .views import *
urlpatterns = [
    path('vid/<int:id>/', vidView, name='vid-view')

]