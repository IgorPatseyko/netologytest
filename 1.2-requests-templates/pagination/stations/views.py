from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv
from django.conf import settings


def index(request):
    return redirect(reverse('bus_stations'))


DATA = []
with open(settings.BUS_STATION_CSV, newline='', encoding='utf8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        DATA.append({
            'Name': row['Name'],
            'Street': row['Street'],
            'District': row['District']
        })


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(DATA, 10)
    page = paginator.get_page(page_number)
    context = {
         'bus_stations': page.object_list,
         'page': page,
    }
    return render(request, 'stations/index.html', context)
