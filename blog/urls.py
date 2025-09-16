from django.urls import path
from . import views

urlpatterns = [

    # ---------------- BLOGS ----------------
    path("blogs/", views.BlogListView.as_view(), name="blog_list"),
    path("blogs/add/", views.BlogCreateView.as_view(), name="blog_add"),
    path("blogs/<int:pk>/", views.BlogDetailView.as_view(), name="blog_detail"),
    path("blogs/<int:pk>/edit/", views.BlogUpdateView.as_view(), name="blog_edit"),
    path("blogs/<int:pk>/delete/", views.BlogDeleteView.as_view(), name="blog_delete"),

]
