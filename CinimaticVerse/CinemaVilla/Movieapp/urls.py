from django.urls import path
from .views import profile, profile_edit
from . import views

urlpatterns = [
    path('',views.func,name = 'func'),
    path('login/',views.login,name='login'),
    path('signup/',views.register,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/',views.profile,name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),


    #movie
    path('add/', views.add_movie, name='add_movie'),
    path('<int:movie_id>/edit/',views.edit_movie, name='edit_movie'),
    path('<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    path('movie_details/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('search/', views.search_view, name='search_view'),

]