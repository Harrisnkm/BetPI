from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('margins/', views.margins, name='margins'),
    path('resources/', views.resources, name='resources')
]