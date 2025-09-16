from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from course.models import Course
from .models import Category, Blog
from .forms import CategoryForm, BlogForm


# ---------------- CATEGORY ----------------
class CategoryListView(ListView):
    model = Category
    template_name = "categories/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "categories/category_detail.html"
    context_object_name = "category"


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    success_url = reverse_lazy("category_list")


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    success_url = reverse_lazy("category_list")


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "categories/category_confirm_delete.html"
    success_url = reverse_lazy("category_list")


# ---------------- BLOG ----------------
class BlogListView(ListView):
    model = Blog
    template_name = "blogs/blog_list.html"
    context_object_name = "blogs"


class BlogDetailView(DetailView):
    model = Blog
    template_name = "blogs/blog_detail.html"
    context_object_name = "blog"


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = "blogs/blog_form.html"
    success_url = reverse_lazy("blog_list")


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "blogs/blog_form.html"
    success_url = reverse_lazy("blog_list")


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = "blogs/blog_confirm_delete.html"
    success_url = reverse_lazy("blog_list")

