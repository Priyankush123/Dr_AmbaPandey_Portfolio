from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import Paper
import os

BASE_DIR = os.path.join("core", "seed_pdfs")

class Command(BaseCommand):
    help = "Import PDFs into database"

    def handle(self, *args, **kwargs):
        for category, folder in [
            ("book", "books"),
            ("publication", "publications")
        ]:
            folder_path = os.path.join(BASE_DIR, folder)

            if not os.path.exists(folder_path):
                continue

            for filename in os.listdir(folder_path):
                if filename.lower().endswith(".pdf"):
                    full_path = os.path.join(folder_path, filename)

                    with open(full_path, "rb") as f:
                        Paper.objects.get_or_create(
                            title=filename.replace(".pdf", "").replace("_", " ").title(),
                            category=category,
                            pdf=File(f, name=filename),
                        )

        self.stdout.write(self.style.SUCCESS("PDFs imported successfully"))
