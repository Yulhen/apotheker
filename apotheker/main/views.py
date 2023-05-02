from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Drug, Receipt, ReceiptSchedule
from .forms import DrugForm, ReceiptForm, NewUserForm


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


@login_required(login_url='main:login')
def list_drugs(request: HttpRequest) -> HttpResponse:
    context = {
        'drugs': Drug.objects.all(),
    }
    return render(request, 'list_drugs.html', context)


@login_required(login_url='main:login')
def add_drug(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.POST:
        drug_form = DrugForm(request.POST)
        if drug_form.is_valid():
            drug = Drug.objects.create(
                name=drug_form.data['name'],
                description=drug_form.data['description'],
            )
            drug.save()
            context['created_drug'] = drug
        else:
            context['form_errors'] = drug_form.errors
    return render(request, 'add_drug.html', context)


@login_required(login_url='main:login')
def delete_drug(request: HttpRequest, drug_id: int) -> HttpResponse:
    drug = Drug.objects.get(id=drug_id)
    # deleted_drug = drug.name
    drug.delete()
    return redirect('main:list_drugs')


@login_required(login_url='main:login')
def add_receipt(request: HttpRequest) -> HttpResponse:
    context = {
        'drugs': Drug.objects.all(),
    }

    if request.POST:
        receipt_form = ReceiptForm(request.POST)
        if receipt_form.is_valid():
            receipt = Receipt.objects.create(
                user=request.user,
                drug=Drug.objects.get(id=receipt_form.data['drug']),
                days=receipt_form.data['days'],
                start_dt=receipt_form.data['start_dt'],
            )
            receipt.save()

            for time, amount in zip(request.POST.getlist('time', []), request.POST.getlist('amount', [])):
                schedule = ReceiptSchedule.objects.create(
                    time=time,
                    amount=amount,
                    receipt=receipt,
                )
                schedule.save()

            context['created_receipt'] = receipt
        else:
            context['form_errors'] = receipt_form.errors
    return render(request, 'add_receipt.html', context)


@login_required(login_url='main:login')
def list_receipts(request: HttpRequest) -> HttpResponse:
    receipts = [r for r in Receipt.objects.filter(user=request.user)  if r.end_dt >= datetime.now().date() and r.is_closest_medication_today]
    context = {
        'receipts': sorted(receipts, key=lambda r: r.closest_medication.time),
    }

    return render(request, 'list_receipts.html', context)

@login_required(login_url='main:login')
def logout_request(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('main:index')


def register_request(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def faq(request: HttpRequest) -> HttpResponse:
    return render(request, 'faq.html')


def contacts(request: HttpRequest) -> HttpResponse:
    return render(request, 'contacts.html')