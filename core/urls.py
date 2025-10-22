from django.urls import path
from core import views

app_name="core"

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("demo/loading", views.demo_loading, name="demo_loading"),
]