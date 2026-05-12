from django.shortcuts import render,redirect
from  ManageCash.forms import *
from ManageCash.models import *
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

# Create your views here.

def register_page(request):
    if request.method == 'POST':
        form_data=RegisterForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,'Registration Successful')
            return redirect('login_page')
    form_data=RegisterForm()
    context={
        'form_data': form_data,
        'form_title':'Register Form',
        'form_btn':'Register'
        
    }
    
    return render (request, 'master/base-form.html',context)

def login_page (request):
    if request.method == 'POST':
        form_data=LoginForm(request,request.POST)
        if form_data.is_valid():
            user=form_data.get_user()
            login(request,user)
            messages.success(request,'Login Successful')
            return redirect('dashboard_page')
    
    form_data=LoginForm()
    context={
        'form_data': form_data,
        'form_title':'Login Form',
        'form_btn':'LogIn'
        
    }
    
    return render (request,'master/base-form.html',context)

@login_required
def logout_page(request):
    logout(request)
    messages.success(request,'Logout Successful')
    return redirect('login_page')

@login_required
def dashboard_page(request):
    cash_data=CashModel.objects.filter(user=request.user)
    expense_data=ExpenseModel.objects.filter(user=request.user)
    
    total_cash=cash_data.aggregate(total=Sum('amount'))['total'] or 0
    total_expense=expense_data.aggregate(total=Sum('amount'))['total'] or 0
    
    current_balance=round(total_cash-total_expense,2)
    
    context={
        'total_cash':total_cash,
        'total_expense': total_expense,
        'current_balance':current_balance
        
    }
    
    return render (request,'dashboard.html',context)

@login_required
def cash_list(request):
    form_data=CashModel.objects.filter(user=request.user)
    context={
        'form_data':form_data
    }
    
    return render(request,'cash-list.html',context)

def add_cash(request):
    if request.method == 'POST':
        form_data=CashForm(request.POST)
        if form_data.is_valid():
            data=form_data.save(commit=False)
            data.user=request.user
            data.save()
            messages.success(request,'Data Added Succesfully')
            return redirect('cash_list')
            
    form_data=CashForm()
    
    context={
        'form_data': form_data,
        'form_title':'Add Cash Details',
        'form_btn':'Add Cash'
        
    }
    
    return render (request,'master/base-form.html',context)

def update_cash(request,id):
    data=CashModel.objects.get(id=id)
    if request.method == 'POST':
        form_data=CashForm(request.POST,instance=data)
        if form_data.is_valid():
            data=form_data.save(commit=False)
            data.user=request.user
            data.save()
            messages.success(request,'Data Added Succesfully')
            return redirect('cash_list')
            
    form_data=CashForm(instance=data)
    
    context={
        'form_data': form_data,
        'form_title':'Update Cash Details',
        'form_btn':'Update Cash'
    }
    return render(request,'master/base-form.html',context)

def delete_page(request,id):
    CashModel.objects.get(id=id).delete()
    messages.success(request,'Delete Successful')
    return redirect('cash_list')
@login_required
def expense_page(request):
    form_data=ExpenseModel.objects.filter(user=request.user)
    context={
        'form_data':form_data
    }
    
    return render (request,'expense-list.html',context)

def add_expense(request):
    if request.method == 'POST':
        form_data=ExpenseForm(request.POST)
        if form_data.is_valid():
            data=form_data.save(commit=False)
            data.user=request.user
            data.save()
            messages.success(request,'Data Added Succesfully')
            return redirect('expense_page')
            
    form_data=ExpenseForm()
    
    context={
        'form_data': form_data,
        'form_title':'Add Expense Details',
        'form_btn':'Add Expense'
        
    }
    return render(request,'master/base-form.html',context)

def update_expense(request,id):
    data=ExpenseModel.objects.get(id=id)
    if request.method == 'POST':
        form_data=ExpenseForm(request.POST,instance=data)
        if form_data.is_valid():
            data=form_data.save(commit=False)
            data.user=request.user
            data.save()
            messages.success(request,'Data Added Succesfully')
            return redirect('expense_page')
            
    form_data=ExpenseForm(instance=data)
    
    context={
        'form_data': form_data,
        'form_title':'Update Expense Details',
        'form_btn':'Update Expense'
    }
    return render(request,'master/base-form.html',context)

def delete_expense(request,id):
    ExpenseModel.objects.get(id=id).delete()
    messages.success(request,'Delete Successful')
    return redirect('expense_page')