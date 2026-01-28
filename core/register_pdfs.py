import os
from core.models import Paper

BASE_PATH = "media/pdfs"

BOOKS_PATH = os.path.join(BASE_PATH, "books")
PUBS_PATH = os.path.join(BASE_PATH, "publications")

# BOOKS
for filename in os.listdir(BOOKS_PATH):
    if filename.lower().endswith(".pdf"):
        Paper.objects.get_or_create(
            title=filename.replace(".pdf", "").replace("_", " ").title(),
            pdf=f"pdfs/books/{filename}",
            category="book"
        )

# PUBLICATIONS
for filename in os.listdir(PUBS_PATH):
    if filename.lower().endswith(".pdf"):
        Paper.objects.get_or_create(
            title=filename.replace(".pdf", "").replace("_", " ").title(),
            pdf=f"pdfs/publications/{filename}",
            category="publication"
        )

print(" All PDFs registered successfully")
