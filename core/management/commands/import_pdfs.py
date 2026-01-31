import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from core.models import Paper


class Command(BaseCommand):
    help = "Import PDFs into PostgreSQL database"

    def handle(self, *args, **kwargs):

        #  Safety Check — NEVER import into SQLite
        if not os.environ.get("DATABASE_URL"):
            raise Exception(" DATABASE_URL not found. Aborting import.")

        self.stdout.write(" DATABASE_URL detected. Using PostgreSQL.")

        BASE_DIR = os.path.join(settings.BASE_DIR, "core", "seed_pdfs")

        self.stdout.write(f" Looking for seed folder at:")
        self.stdout.write(BASE_DIR)

        if not os.path.exists(BASE_DIR):
            self.stdout.write(" seed_pdfs folder NOT found.")
            return

        total_created = 0

        categories = [
            ("book", "books"),
            ("publication", "publications"),
        ]

        for category_value, folder_name in categories:

            folder_path = os.path.join(BASE_DIR, folder_name)

            self.stdout.write(f"\n Checking folder: {folder_path}")

            if not os.path.exists(folder_path):
                self.stdout.write(" Folder missing — skipping.")
                continue

            files = os.listdir(folder_path)

            self.stdout.write(f" Found {len(files)} files")

            for filename in files:

                if not filename.lower().endswith(".pdf"):
                    continue

                full_path = os.path.join(folder_path, filename)

                title = (
                    filename.replace(".pdf", "")
                    .replace("_", " ")
                    .title()
                )

                #  Prevent duplicates
                if Paper.objects.filter(title=title).exists():
                    self.stdout.write(f" Already exists: {title}")
                    continue

                try:
                    with open(full_path, "rb") as f:

                        paper = Paper.objects.create(
                            title=title,
                            category=category_value,
                            pdf=File(f, name=filename),
                        )

                        total_created += 1
                        self.stdout.write(f" Created: {paper.title}")

                except Exception as e:
                    self.stdout.write(f" Failed to import {filename}")
                    self.stdout.write(str(e))

        self.stdout.write("\n==============================")
        self.stdout.write(
            self.style.SUCCESS(
                f" IMPORT COMPLETE — {total_created} PDFs added."
            )
        )
        self.stdout.write(
            f" Total Papers in DB now: {Paper.objects.count()}"
        )
