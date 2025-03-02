from django.urls import path
from . import views




urlpatterns = [
path("counters/", views.CounterList.as_view(), name="Counters"),
path("counters/<str:id>/", views.CounterDetails.as_view(), name="Counter-Details"),
path("register/", views.RegisterView().as_view(), name="Register"),
path("login/", views.LoginView.as_view(), name="Login"),

]