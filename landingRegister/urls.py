
from . import views
from django.urls import path, include



app_name = 'landingRegister'


urlpatterns = [
    path("contactus", views.ContactUsView.as_view(), name="contactus"),

    path("comingsoon", views.comingsoon, name="comingsoon"),


    path('register', views.RegistrationView.as_view(), name='register'),

    path('activate/<uidb64>/<token>',
        views.ActivateAccountView.as_view(), name='activate'),
        
    path('set-new-password/<uidb64>/<token>',
        views.SetNewPasswordView.as_view(), name='set-new-password'),

    path('request-reset-email', views.RequestResetEmailView.as_view(),
        name='request-reset-email'),

    path("dashboard/", views.graphsView, name="dashboard"),
]
