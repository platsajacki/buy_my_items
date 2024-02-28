import csv
from typing import Any

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Model

from items.models import Tax
from orders.models import Discount

DATA_DIR: str = f'{settings.BASE_DIR}/static/data'


class Command(BaseCommand):
    help: str = 'Imports data from CSV files into the database'

    def handle(self, *args: Any, **options: Any) -> None:
        self.import_coupons()
        self.import_product_tax_codes()

    def import_data_from_csv(self, file_path: str, model_class: Model, field_names: list[str]) -> None:
        with open(file_path, 'r') as csv_file:
            next(reader := csv.reader(csv_file))
            for row in reader:
                data: dict[str, str] = dict(zip(field_names, row))
                instance = model_class.objects.filter(**data)
                if not instance.exists():
                    instance.create(**data)
                    self.stdout.write(
                        self.style.SUCCESS(f'Data imported successfully: {data['id']}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Data already exists: {data['id']}')
                    )

    def import_coupons(self) -> None:
        self.import_data_from_csv(f'{DATA_DIR}/coupons.csv', Discount, ['id'])

    def import_product_tax_codes(self) -> None:
        self.import_data_from_csv(f'{DATA_DIR}/product_tax_codes.csv', Tax, ['id', 'type', 'description', 'name'])
