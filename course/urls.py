from django.urls import path
from . import views

urlpatterns = [
    # ---------------- COURSES ----------------
    path("courses/", views.CourseListView.as_view(), name="course_list"),
    path("courses/add/", views.CourseCreateView.as_view(), name="course_add"),
    path("courses/<int:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("courses/<int:pk>/edit/", views.CourseUpdateView.as_view(), name="course_edit"),
    path("courses/<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course_delete"),

    # ---------------- SUBSCRIBERS ----------------
    path("subscribers/", views.SubscriberListView.as_view(), name="subscriber_list"),
    path("subscribers/add/", views.SubscriberCreateView.as_view(), name="subscriber_add"),
    path("subscribers/<int:pk>/delete/", views.SubscriberDeleteView.as_view(), name="subscriber_delete"),

    # ---------------- EXPERTS ----------------
    path("experts/", views.ExpertListView.as_view(), name="expert_list"),
    path("experts/add/", views.ExpertCreateView.as_view(), name="expert_add"),
    path("experts/<int:pk>/", views.ExpertDetailView.as_view(), name="expert_detail"),
    path("experts/<int:pk>/edit/", views.ExpertUpdateView.as_view(), name="expert_edit"),
    path("experts/<int:pk>/delete/", views.ExpertDeleteView.as_view(), name="expert_delete"),

    path("courses/<int:course_id>/learn/", views.AddLearningOutcomeView.as_view(), name="whatstudentwillearn_add"),

]
