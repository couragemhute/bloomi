from django.urls import path
from .views import *

urlpatterns = [
    # ---------------- COURSES ----------------
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/add/", CourseCreateView.as_view(), name="course_add"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("courses/<int:pk>/edit/", CourseUpdateView.as_view(), name="course_edit"),
    path("courses/<int:pk>/delete/", CourseDeleteView.as_view(), name="course_delete"),

    # ---------------- SUBSCRIBERS ----------------
    path("subscribers/", SubscriberListView.as_view(), name="subscriber_list"),
    path("subscribers/add/", SubscriberCreateView.as_view(), name="subscriber_add"),
    path("subscribers/<int:pk>/delete/", SubscriberDeleteView.as_view(), name="subscriber_delete"),

    # ---------------- EXPERTS ----------------
    path("experts/", ExpertListView.as_view(), name="expert_list"),
    path("experts/add/", ExpertCreateView.as_view(), name="expert_add"),
    path("experts/<int:pk>/", ExpertDetailView.as_view(), name="expert_detail"),
    path("experts/<int:pk>/edit/", ExpertUpdateView.as_view(), name="expert_edit"),
    path("experts/<int:pk>/delete/", ExpertDeleteView.as_view(), name="expert_delete"),

    path("courses/<int:course_id>/learn/", AddLearningOutcomeView.as_view(), name="whatstudentwillearn_add"),

    path('course-rating/index/', CourseRatingListView.as_view(), name="course-rating-index"), 
    path('course-rating/create/', CourseRatingCreateView.as_view(), name="course-rating-create"),  
    path('course-rating/update/<int:pk>/', CourseRatingUpdateView.as_view(), name="course-rating-update"), 
    path('course-rating/details/<int:pk>/', CourseRatingDetailsView.as_view(), name="course-rating-details"), 
    path('course-rating/delete/<int:pk>/', CourseRatingDeleteView.as_view(), name="course-rating-delete"),

]
