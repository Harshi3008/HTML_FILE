import os
from django.core.management.base import BaseCommand
from Land.models import Book
import openpyxl

class Command(BaseCommand):
    help = 'Import books from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file to import')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        if not os.path.exists(excel_file):
            self.stdout.write(self.style.ERROR(f"File {excel_file} does not exist"))
            return

        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        # Assuming the Excel columns are:
        # Title | Category | Description | Price | Author | Available Copies
        # Starting from row 2 (row 1 is header)
        imported_count = 0
        for row in sheet.iter_rows(min_row=2, values_only=True):
            title, category, description, price, author, available_copies = row
            if not title:
                continue
            book, created = Book.objects.update_or_create(
                title=title,
                defaults={
                    'category': category or '',
                    'description': description or '',
                    'price': str(price) if price is not None else '',
                    'author': author or '',
                    'available_copies': int(available_copies) if available_copies else 1,
                }
            )
            if created:
                imported_count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported or updated {imported_count} books from {excel_file}"))
