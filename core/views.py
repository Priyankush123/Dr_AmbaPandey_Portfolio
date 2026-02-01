from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from datetime import timedelta
import random
import os
from django.views.decorators.http import require_POST
from .models import Visitor, Paper, AccessLog
from core.models import AcademicSection
from .models import BlogPost
from .models import GalleryEvent, GalleryImage
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.http import HttpResponse

# ==========================
# HELPERS
# ==========================
def is_logged_in(request):
    return request.session.get("visitor_id") is not None


def is_admin(request):
    return request.session.get("visitor_email") == settings.ADMIN_EMAIL

def create_admin_once(request):
    if User.objects.filter(username="admin").exists():
        return HttpResponse("Admin already exists")

    User.objects.create_superuser(
        username="admin",
        email="biswaspriyankush@gmail.com",
        password="Priyankush@123"
    )
    return HttpResponse("Admin created")
# ==========================
# PAGE VIEWS
# ==========================
def home(request):
    books = Paper.objects.filter(category="book")
    publications = Paper.objects.filter(category="publication")

    blogs = BlogPost.objects.filter(is_published=True)
    gallery_events = GalleryEvent.objects.prefetch_related("images")
    return render(
        request,
        "index.html",
        {
            "books": books,
            "publications": publications,
            "blogs": blogs,
            "gallery_events": gallery_events
        }
    )
def api_public_blogs(request):
    blogs = BlogPost.objects.filter(is_published=True).order_by("-created_at")

    return JsonResponse({
        "blogs": [
            {
                "id": b.id,
                "title": b.title,
                "summary": b.summary,
                "image": b.image.url if b.image else "",
                "created_at": b.created_at.strftime("%d %b %Y"),
            }
            for b in blogs
        ]
    })

@csrf_exempt
def admin_blog_create(request):
    if not request.session.get("is_admin"):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    BlogPost.objects.create(
        title=request.POST.get("title"),
        summary=request.POST.get("summary"),
        content=request.POST.get("content"),
        image=request.FILES.get("image"),
        is_published=True,
    )

    return JsonResponse({"status": "created"})

@csrf_exempt
def admin_blog_update(request, blog_id):
    if not request.session.get("is_admin"):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    blog = get_object_or_404(BlogPost, id=blog_id)

    blog.title = request.POST.get("title")
    blog.summary = request.POST.get("summary")
    blog.content = request.POST.get("content")

    if request.FILES.get("image"):
        blog.image = request.FILES["image"]

    blog.save()
    return JsonResponse({"status": "updated"})


@csrf_exempt
def admin_blog_delete(request, blog_id):
    if not request.session.get("is_admin"):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    BlogPost.objects.filter(id=blog_id).delete()
    return JsonResponse({"status": "deleted"})

def admin_blog_list(request):
    blogs = BlogPost.objects.all()
    return JsonResponse({
        "blogs": [
            {
                "id": b.id,
                "title": b.title,
                "summary": b.summary,
                "content": b.content,
            }
            for b in blogs
        ]
    })


def api_blog_detail(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id, is_published=True)

    return JsonResponse({
        "title": blog.title,
        "content": blog.content,
        "image": blog.image.url if blog.image else "",
        "created_at": blog.created_at.strftime("%d %b %Y"),
    })



def register_view(request):
    return render(request, "register.html")


def login_view(request):
    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    return redirect("home")

# ==========================
# OTP REGISTRATION
# ==========================
@csrf_exempt
def send_otp(request):
    if request.method != "POST":
        return JsonResponse({"status": "invalid_method"}, status=405)

    email = request.POST.get("email")
    if not email:
        return JsonResponse({"status": "email_missing"}, status=400)

    visitor, _ = Visitor.objects.get_or_create(email=email)

    if visitor.is_verified:
        return JsonResponse({"status": "already_registered"})

    otp = str(random.randint(100000, 999999))
    visitor.otp = otp
    visitor.save()

    # ❌ DO NOT SEND EMAIL HERE ON RENDER FREE
    # Email will be added later via background worker / service

    print(f"✅ OTP generated for {email}: {otp}")

    return JsonResponse({"status": "otp_sent"})




@csrf_exempt
def verify_otp_and_register(request):
    if request.method != "POST":
        return JsonResponse({"status": "invalid_method"})

    name = request.POST.get("name")
    email = request.POST.get("email")
    otp = request.POST.get("otp")

    if not all([name, email, otp]):
        return JsonResponse({"status": "missing_fields"})

    try:
        visitor = Visitor.objects.get(email=email)
    except Visitor.DoesNotExist:
        return JsonResponse({"status": "email_not_found"})

    if visitor.otp != otp:
        return JsonResponse({"status": "wrong_otp"})

    visitor.name = name
    visitor.is_verified = True
    visitor.otp = None
    visitor.save()

    return JsonResponse({"status": "verified"})

# ==========================
# LOGIN
# ==========================
@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"status": "invalid_method"})

    email = request.POST.get("email")
    name = request.POST.get("name")

    if not email or not name:
        return JsonResponse({"status": "missing_fields"})

    try:
        visitor = Visitor.objects.get(email=email, is_verified=True)
    except Visitor.DoesNotExist:
        return JsonResponse({"status": "not_registered"})

    # 🔒 BLOCK CHECK
    if visitor.blocked_until and visitor.blocked_until > timezone.now():
        return JsonResponse({
            "status": "temporarily_blocked",
            "blocked_until": visitor.blocked_until.isoformat()
        })

    # Update last login
    visitor.last_login = timezone.now()
    visitor.save()

    # SESSION
    request.session["visitor_id"] = visitor.id
    request.session["visitor_email"] = visitor.email
    request.session["visitor_name"] = visitor.name
    request.session["is_admin"] = (visitor.email == settings.ADMIN_EMAIL)

    return JsonResponse({"status": "logged_in"})


# ==========================
# PDF VIEW (PROTECTED)
# ==========================
def view_pdf(request, paper_id):
    if not is_logged_in(request):
        return redirect("login")

    paper = get_object_or_404(Paper, id=paper_id)

    AccessLog.objects.create(
        visitor_id=request.session["visitor_id"],
        paper=paper
    )

    return redirect(paper.pdf.url)

# ==========================
# ADMIN DASHBOARD
# ==========================
def admin_dashboard(request):
    if not is_logged_in(request):
        return redirect("login")

    if not is_admin(request):
        return JsonResponse({"status": "forbidden"}, status=403)

    query = request.GET.get("q", "").strip()

    logs = AccessLog.objects.select_related("visitor", "paper").order_by("-accessed_at")
    users = Visitor.objects.filter(is_verified=True).order_by("-last_login")
    gallery_events = GalleryEvent.objects.prefetch_related("images")
    if query:
        logs = logs.filter(
            Q(visitor__email__icontains=query) |
            Q(paper__title__icontains=query)
        )
    
    papers = Paper.objects.all().order_by("-id")

    return render(
        request,
        "admin_dashboard.html",
        {
            "logs": logs,
            "users": users,
            "papers": papers,
            "query": query,
            "now": timezone.now(),
            "gallery_events": gallery_events,
        }
    )

def admin_upload_pdf(request):
    if not request.session.get("visitor_id") or not request.session.get("is_admin"):
        return redirect("/login/")

    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")
        pdf_file = request.FILES.get("pdf")

        if not all([title, category, pdf_file]):
            messages.error(request, "All fields are required")
            return redirect("admin_upload_pdf")

        Paper.objects.create(
            title=title,
            category=category,
            pdf=pdf_file
        )

        messages.success(request, "PDF uploaded successfully")
        return redirect("admin_dashboard")

    return render(request, "admin_upload.html")

def admin_edit_pdf(request, paper_id):
    if not request.session.get("is_admin"):
        return redirect("/login/")

    paper = get_object_or_404(Paper, id=paper_id)

    if request.method == "POST":
        paper.title = request.POST.get("title")
        paper.category = request.POST.get("category")

        if request.FILES.get("pdf"):
            paper.pdf.delete(save=False)
            paper.pdf = request.FILES["pdf"]

        paper.save()
        return redirect("admin_dashboard")

    return render(request, "admin_edit_pdf.html", {"paper": paper})

@require_POST
def admin_delete_pdf(request, paper_id):
    if not request.session.get("is_admin"):
        return JsonResponse({"status": "forbidden"}, status=403)

    paper = get_object_or_404(Paper, id=paper_id)
    paper.pdf.delete(save=False)
    paper.delete()

    return JsonResponse({"status": "deleted"})

# ==========================
# BLOCK / UNBLOCK USER
# ==========================
@csrf_exempt
def toggle_block_user(request, visitor_id):
    if not is_admin(request):
        return JsonResponse({"status": "forbidden"}, status=403)

    visitor = get_object_or_404(Visitor, id=visitor_id)

    if visitor.blocked_until and visitor.blocked_until > timezone.now():
        visitor.blocked_until = None
        status = "unblocked"
    else:
        visitor.blocked_until = timezone.now() + timedelta(hours=1)
        status = "blocked"

    visitor.save()
    return JsonResponse({"status": status})

def admin_gallery_dashboard(request):
    if not request.session.get("is_admin"):
        return redirect("login")

    events = GalleryEvent.objects.prefetch_related("images").order_by("-created_at")
    return render(request, "admin/gallery_dashboard.html", {"events": events})

def admin_gallery_add(request):
    if not request.session.get("is_admin"):
        return redirect("login")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        images = request.FILES.getlist("images")

        if not title or not images:
            messages.error(request, "Title and images are required")
            return redirect("admin_dashboard")

        event = GalleryEvent.objects.create(
            title=title,
        )

        for img in images:
            GalleryImage.objects.create(
                event=event,
                image=img
            )

        messages.success(request, "Event added successfully")

    return redirect("admin_dashboard")


def admin_gallery_delete(request, event_id):
    if not request.session.get("is_admin"):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    GalleryEvent.objects.filter(id=event_id).delete()
    return JsonResponse({"status": "deleted"})







