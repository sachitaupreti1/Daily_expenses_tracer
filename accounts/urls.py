from django.urls import path
from . import views

urlpatterns = [
    # Auth & Dashboard
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout"),

    # Add Income / Expense
    path('add-income/', views.add_income, name='add_income'),
    path('add-expenses/', views.add_expenses, name='add_expenses'),

    # Edit Income / Expense
    path('edit-income/<int:id>/', views.edit_income, name='edit_income'),
   path('edit-expense/<int:id>/', views.edit_expense, name='edit_expense'),


    # Delete Income / Expense
    path('delete-income/<int:id>/', views.delete_income, name='delete_income'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),



    # All transactions
    path('all-transactions/', views.all_transactions, name='all_transactions'),

    # Income / Expenses list pages (plural)
    path('income/', views.income, name='income'),
    path('expenses/', views.expense, name='expenses'),  # plural
]
