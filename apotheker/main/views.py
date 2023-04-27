from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Drug
from .forms import DrugForm


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


def list_drugs(request: HttpRequest) -> HttpResponse:
    context = {
        'drugs': Drug.objects.all(),
    }
    return render(request, 'list_drugs.html', context)


def add_drug(request: HttpRequest) -> HttpResponse:
    if request.POST:
        drug_form = DrugForm(request.POST)
        if drug_form.is_valid():
            drug = Drug.objects.create(
                name=drug_form.data['name'],
                description=drug_form.data['description'],
            )
            drug.save()
    return render(request, 'add_drug.html')

