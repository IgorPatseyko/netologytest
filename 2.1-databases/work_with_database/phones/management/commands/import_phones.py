import csv
from datetime import datetime
from datetime import timezone


from django.core.management.base import BaseCommand
from django.utils.text import slugify

from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))
        #print(phones)
        for phone in phones:
            Phone.objects.create(
                id=int(phone['id']),
                name=phone['name'],
                image=phone['image'],
                price=int(phone['price']),
                release_date=datetime.strptime(phone['release_date'], '%Y-%m-%d').replace(tzinfo=timezone.utc),
                lte_exists=eval(phone['lte_exists']),
                #slug=slugify(Phone, )
            )
            # TODO: Добавьте сохранение модели
