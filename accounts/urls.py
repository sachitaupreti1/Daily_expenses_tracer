from django.urls import path
from . import views

urlpatterns = [
  
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout"),

    path('add-income/', views.add_income, name='add_income'),
    path('add-expenses/', views.add_expenses, name='add_expenses'),

    path('edit-income/<int:id>/', views.edit_income, name='edit_income'),
   path('edit-expense/<int:id>/', views.edit_expense, name='edit_expense'),

    path('delete-income/<int:id>/', views.delete_income, name='delete_income'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),

    path('all-transactions/', views.all_transactions, name='all_transactions'),

    path('income/', views.income, name='income'),
    path('expenses/', views.expense, name='expenses'),  # plural
]
