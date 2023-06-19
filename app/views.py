import re

import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from google_play_scraper import app

from .models import Package, PackageDetail


def scrape_playstore(request):
    url = 'https://play.google.com/store/games?hl=en&gl=US'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pattern = r'^/store/apps/details\?id=com.*.*$'
    all_anchor_tag = soup.find_all('a')
    for anchor_tag in all_anchor_tag:
        data = anchor_tag['href']
        if re.match(pattern,data):
            package_db =Package.objects.filter(name = data.split('=')[1]).first()
            if package_db:
                pass
            else:
                package = Package(name=data.split('=')[1])
                package.save()

                package_info = app(data.split('=')[1])
                package_detail = PackageDetail(package=package)
                package_detail.title = package_info['title']
                package_detail.save()

    return JsonResponse({'status': 'success'})


def get_package_details(request, package_name):
    try:
        package = Package.objects.get(name=package_name)
        package_detail, created = PackageDetail.objects.get_or_create(package=package)

        if created:
            package_info = app(package_name)
            package_detail.title = package_info['title']

            package_detail.save()

        return JsonResponse({'status': 'success', 'data': {
            'title': package_detail.title
        }})

    except Package.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Package not found'})


def get_all_packages(request):
    packages = Package.objects.all()
    package_data = [{'name': package.name} for package in packages]
    return JsonResponse({'status': 'success', 'data': package_data})
