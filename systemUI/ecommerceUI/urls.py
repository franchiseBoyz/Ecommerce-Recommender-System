from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('search/', views.search_view, name='search'),  # Search results page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('login/', auth_views.LoginView.as_view(template_name='products/login.html', next_page='home'), name='login'),  # Redirect to home after login
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Redirect to home after logout
    path('recommendations/', views.search_view, name='recommendations'),  # Recommendations page
]