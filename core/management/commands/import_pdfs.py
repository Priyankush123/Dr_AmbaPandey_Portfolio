import os
from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import Paper

class Command(BaseCommand):
    help = "Import PDFs into database"

    def handle(self, *args, **kwargs):
        if not os.environ.get("DATABASE_URL"):
            raise Exception(" DATABASE_URL not set. Aborting import.")

        self.stdout.write(" DATABASE_URL detected. Using PostgreSQL.")
        self.stdout.write(f" Papers in DB after import: {Paper.objects.count()}")