from django.urls import path
from .views import *
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import (
    MyPasswordResetView,
    MyPasswordResetDoneView,
    MyPasswordResetConfirmView,
    MyPasswordResetCompleteView,
)
from . import views

urlpatterns = [
    path('administration/',administration, name="administration"),
    path('users/',users, name="users"),
    path('dashboard/', dashboard, name='dashboard'),
    
    path('<int:recette_id>/', views.recette_detail, name='recette_detail'),
    path('signup/',signUp, name="signup"),
    path('',logIn, name="login"),
    path('index/',Index, name="index"),
    path('logout/',logOut, name="logout"),
    path('about/', aboutUs, name="about"),
    path('commentaires/', commentaires, name='commentaires'),
    path('user_account/', userAccount, name="user_account"),
    path('profile/', user_profile, name='user_profile'),
    path('index1/', recettes_view, name='recettes'),
    path('search/', views.search_recipes, name='search_recipes'),
    path('ajouter_commentaire/', ajouter_commentaire, name='ajouter_commentaire'),
    path('ajouter_rank/<int:recette_id>/',  ajouter_rank, name='ajouter_rank'),

    path('recette/<int:recette_id>/', recette_detail, name='recette_detail'),

    
    path('reset_password/', MyPasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/',MyPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',MyPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/',MyPasswordResetCompleteView.as_view(), name="password_reset_complete"),


    path('add_recipe/', add_recipe_view, name='add_recipe'),
    path('delete/<str:pk>/', deleteRecipe, name="deleteRecipe"),
    path('update/<str:pk>/',updateRecipe, name="updateRecipe"),


    path('add_user/', add_user, name='add_user'),
    path('delete_user/<str:pk>/', deleteUser, name="deleteUser"),
    path('update_user/<str:pk>/',updateUser, name="updateUser"),
    
    
]
