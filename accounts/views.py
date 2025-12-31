from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import Income
from .models import Expenses


# Dashboard view


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "accounts/dashboard.html")

# Login view


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Username or Password")
    return render(request, "accounts/login.html")

# Register view (placeholder)


def register(request):
    return render(request, "accounts/register.html")

# Logout view


def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('login')
    return render(request, "accounts/logout.html")


# def add_expenses(request):
    # return render(request, 'accounts/add_expenses.html')  # lowercase file name
def add_expenses(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        date = request.POST.get("date")
        description = request.POST.get("description")  # match form

        if not amount or not category or not date:
            messages.error(
                request, "All fields except description are required!")
            return render(request, "accounts/add_expenses.html")

        Expenses.objects.create(
            user=request.user,
            title=description or "No description",  # Use description as title
            amount=amount,
            category=category,
            date=date
        )
        messages.success(request, "Expense added successfully!")
        return redirect("dashboard")

    return render(request, "accounts/add_expenses.html")


# def add_income(request):
#     return render(request, 'accounts/add_income.html')    # lowercase file name

def add_income(request):
    if request.method == "POST":
        source = request.POST.get("source")
        amount = request.POST.get("amount")
        date = request.POST.get("date")

        Income.objects.create(
            user=request.user,
            source=source,
            amount=amount,
            date=date
        )

        messages.success(request, "Income added successfully ✅")
        return redirect("dashboard")

    return render(request, 'accounts/add_income.html')


def all_transactions(request):
    if not request.user.is_authenticated:
        return redirect('login')

    incomes = Income.objects.filter(user=request.user)
    expenses = Expenses.objects.filter(user=request.user)

    transactions = []

    for income in incomes:
        transactions.append({
            'id': income.id,
            'category': income.source,
            'date': income.date,
            'amount': income.amount,
            'payment': getattr(income, 'payment_method', 'N/A'),
            'type': 'Income'
        })

    for expense in expenses:
        transactions.append({
            'id': expense.id,
            'category': expense.category,
            'date': expense.date,
            'amount': expense.amount,
            'payment': getattr(expense, 'payment_method', 'N/A'),
            'type': 'Expense'
        })

    transactions.sort(key=lambda x: x['date'], reverse=True)

    return render(request, 'accounts/all_transactions.html', {
        'transactions': transactions
    })


def edit_income(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    income = Income.objects.get(id=id, user=request.user)

    if request.method == "POST":
        income.source = request.POST.get("source")
        income.amount = request.POST.get("amount")
        income.date = request.POST.get("date")
        income.save()
        return redirect('all_transactions')

    return render(request, 'accounts/edit_income.html', {'income': income})


def delete_income(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    income = get_object_or_404(Income, id=id, user=request.user)
    income.delete()
    return redirect('all_transactions')


def delete_expense(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    expense = get_object_or_404(Expenses, id=id, user=request.user)
    expense.delete()
    return redirect('all_transactions')



def edit_expense(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    expense = Expenses.objects.get(id=id, user=request.user)

    if request.method == "POST":
        expense.title = request.POST.get("title")
        expense.amount = request.POST.get("amount")
        expense.category = request.POST.get("category")
        expense.date = request.POST.get("date")
        expense.save()
        return redirect('all_transactions')

    return render(request, 'accounts/edit_expense.html', {'expense': expense})
