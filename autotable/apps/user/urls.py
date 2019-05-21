from django.urls import path

from .views import LoginView, LogoutView, UserView, AccountView, DataView, IndexContentView

app_name = 'user'

urlpatterns = [
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('info', UserView.as_view(), name="info"),
    path('indexc', IndexContentView.as_view(), name="indexc"),
    path('account', AccountView.as_view(), name="account"),
    path('data', DataView.as_view(), name="data")
]
