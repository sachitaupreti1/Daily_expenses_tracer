from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from datetime import date
from .models import Income, Expense

# =========================
# AUTH & DASHBOARD
# =========================

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "accounts/dashboard.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Username or Password")
    return render(request, "accounts/login.html")


def register(request):
    return render(request, "accounts/register.html")


def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('login')
    return render(request, "accounts/logout.html")


# =========================
# ADD INCOME
# =========================

def add_income(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        category = request.POST.get("category")
        amount = request.POST.get("amount")
        payment_mode = request.POST.get("payment_mode")
        income_date = request.POST.get("date")
        remarks = request.POST.get("remarks", "")

        if not category or not amount or not payment_mode or not income_date:
            messages.error(request, "All fields are required")
            return render(request, "accounts/add_income.html")

        Income.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            payment_mode=payment_mode,
            date=income_date,
            remarks=remarks
        )

        messages.success(request, "Income added successfully ✅")
        return redirect("income")

    return render(request, "accounts/add_income.html")


# =========================
# ADD EXPENSE
# =========================

def add_expenses(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        category = request.POST.get("category")
        amount = request.POST.get("amount")
        payment_mode = request.POST.get("payment_mode")
        expense_date = request.POST.get("date")
        remarks = request.POST.get("remarks", "")

        if not category or not amount or not expense_date:
            messages.error(request, "All fields except remarks are required")
            return redirect('expenses')

        Expense.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            payment_mode=payment_mode,
            date=expense_date,
            remarks=remarks
        )

        messages.success(request, "Expense added successfully ✅")
        return redirect('expenses')

    return redirect('expenses')


# =========================
# ALL TRANSACTIONS
# =========================

def all_transactions(request):
    if not request.user.is_authenticated:
        return redirect('login')

    transactions = []

    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    for income in incomes:
        transactions.append({
            'id': income.id,
            'trans_type': 'income',
            'type': 'Income',
            'category': income.category,
            'date': income.date,
            'amount': income.amount,
            'payment': income.payment_mode,
        })

    for expense in expenses:
        transactions.append({
            'id': expense.id,
            'trans_type': 'expense',
            'type': 'Expense',
            'category': expense.category,
            'date': expense.date,
            'amount': expense.amount,
            'payment': expense.payment_mode,
        })

    transactions.sort(key=lambda x: x['date'], reverse=True)

    return render(request, 'accounts/all_transactions.html', {
        'transactions': transactions,
        'today': date.today()
    })


# =========================
# EDIT INCOME
# =========================

def edit_income(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    income = get_object_or_404(Income, id=id, user=request.user)

    if request.method == "POST":
        income.category = request.POST.get("category")
        income.amount = request.POST.get("amount")
        income.payment_mode = request.POST.get("payment_mode")
        income.date = request.POST.get("date")
        income.remarks = request.POST.get("remarks", "")
        income.save()
        return redirect('income')

    return render(request, 'accounts/edit_income.html', {'income': income})


# =========================
# EDIT EXPENSE
# =========================



def edit_expense(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        expense.category = request.POST.get("category")
        expense.amount = request.POST.get("amount")
        expense.payment_mode = request.POST.get("payment_mode")
        expense.date = request.POST.get("date")
        expense.remarks = request.POST.get("remarks", "")
        expense.save()

        return redirect('expenses')

    return render(request, 'accounts/edit_expense.html', {
        'expense': expense
    })


# =========================
# DELETE INCOME
# =========================

def delete_income(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    income = get_object_or_404(Income, id=id, user=request.user)

    if request.method == "POST":
        income.delete()
        messages.success(request, "Income deleted successfully ✅")
        return redirect('income')

    return render(request, 'accounts/delete.html', {
        'item': income,
        'type': 'Income',
        'category': income.category,
        'payment': income.payment_mode
    })


# =========================
# DELETE EXPENSE
# =========================

def delete_expense(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted successfully ✅")
        return redirect('expenses')

    return render(request, 'accounts/delete.html', {
        'item': expense,
        'type': 'Expense',
        'category': expense.category
    })


# =========================
# INCOME PAGE
# =========================

def income(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        category = request.POST.get("category")
        amount = request.POST.get("amount")
        payment_mode = request.POST.get("payment_mode")
        income_date = request.POST.get("date")
        remarks = request.POST.get("remarks", "")

        if not category or not amount or not payment_mode:
            messages.error(request, "Category, amount, and payment mode are required.")
            return redirect('income')

        Income.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            payment_mode=payment_mode,
            date=income_date or date.today(),
            remarks=remarks
        )

        messages.success(request, "Income added successfully ✅")
        return redirect('income')

    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'accounts/income.html', {
        'incomes': incomes,
        'today': date.today()
    })


# =========================
# EXPENSE PAGE
# =========================

def expense(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        expense_date = request.POST.get("date")
        category = request.POST.get("category")
        amount = request.POST.get("amount")
        payment_mode = request.POST.get("payment_mode")
        remarks = request.POST.get("remarks", "")

        if not category or not amount or not payment_mode:
            messages.error(request, "Category, amount, and payment mode are required.")
            return redirect('expenses')

        Expense.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            payment_mode=payment_mode,
            date=expense_date or date.today(),
            remarks=remarks
        )

        messages.success(request, "Expense added successfully ✅")
        return redirect('expenses')

    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'accounts/expenses.html', {
        'expenses': expenses,
        'today': date.today()
    })
