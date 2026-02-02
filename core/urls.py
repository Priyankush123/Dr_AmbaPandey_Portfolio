from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ==========================
    # PUBLIC PAGES
    # ==========================
    path("", views.home, name="home"),

    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),

    path("api/register/", views.register_user),
    path("api/login/", views.login_user),
    path("logout/", views.logout_view),


    # ==========================
    # PROTECTED RESOURCES
    # ==========================
    path("paper/<int:paper_id>/", views.view_pdf, name="view_pdf"),


    # ==========================
    # ADMIN
    # ==========================
    path("api/admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("api/toggle-block/<int:visitor_id>/", views.toggle_block_user, name="toggle_block"),
    path("admin-upload/", views.admin_upload_pdf, name="admin_upload_pdf"),
    path("admin-edit-pdf/<int:paper_id>/", views.admin_edit_pdf, name="admin_edit_pdf"),
    path("admin-delete-pdf/<int:paper_id>/", views.admin_delete_pdf, name="admin_delete_pdf"),
    # Public blog APIs
    path("api/blogs/", views.api_public_blogs),
    path("api/blogs/<int:blog_id>/", views.api_blog_detail),

    # Admin blog APIs
    path("api/admin/blog/list/", views.admin_blog_list),
    path("api/admin/blog/create/", views.admin_blog_create),
    path("api/admin/blog/update/<int:blog_id>/", views.admin_blog_update),
    path("api/admin/blog/delete/<int:blog_id>/", views.admin_blog_delete),
    path("dashboard/gallery/", views.admin_gallery_dashboard, name="admin_gallery_dashboard"),
    path("dashboard/gallery/add/", views.admin_gallery_add, name="admin_gallery_add"),
    path("dashboard/gallery/delete/<int:event_id>/", views.admin_gallery_delete, name="admin_gallery_delete"),

]
if settings.DEBUG is False:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )