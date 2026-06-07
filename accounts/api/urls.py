from django.urls import path
from .views import (

UserRegistrationView,
LoginView, UpdateRetrieveDeleteUserProfileView,
)

urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('details/me/', UpdateRetrieveDeleteUserProfileView.as_view(), name='user-details'),

]