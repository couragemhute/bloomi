from django.urls import path

from pages.helpers.global_email_sender import contact_form_submission
from .views import (
    AboutTemplateView, BlogTemplateView, ContactTemplateView,
     AiTutorTemplateView, CourseTemplateView,CourseDetailTemplateView, AboutTemplateView,
    Course1TemplateView,
    Course2TemplateView,
    Course3TemplateView,
    Course4TemplateView,
    Course5TemplateView,
    Course6TemplateView,

    Post1TemplateView, Post2TemplateView, Post3TemplateView,
    Post4TemplateView, Post5TemplateView, Post6TemplateView
)

urlpatterns = [
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('blog/', BlogTemplateView.as_view(), name='blog'),
    path('contact/', ContactTemplateView.as_view(), name='contact'),
    path('ai_tutor/', AiTutorTemplateView.as_view(), name='ai_tutor'),

    path('course/', CourseTemplateView.as_view(), name='all_courses'),
    path('course-details/<int:pk>/', CourseDetailTemplateView.as_view(), name='catalogue_course_detail'),


    path('about/', AboutTemplateView.as_view(), name='about'),

    
    path('contact/submit/', contact_form_submission, name='contact_form_submission'),


    path("pages/course/1/", Course1TemplateView.as_view(), name="course_inner_1"),
    path("pages/course/2/", Course2TemplateView.as_view(), name="course_inner_2"),
    path("pages/course/3/", Course3TemplateView.as_view(), name="course_inner_3"),
    path("pages/course/4/", Course4TemplateView.as_view(), name="course_inner_4"),
    path("pages/course/5/", Course5TemplateView.as_view(), name="course_inner_5"),
    path("pages/course/6/", Course6TemplateView.as_view(), name="course_inner_6"),

    path('blog/post/1/', Post1TemplateView.as_view(), name='post-1'),
    path('blog/post/2/', Post2TemplateView.as_view(), name='post-2'),
    path('blog/post/3/', Post3TemplateView.as_view(), name='post-3'),
    path('blog/post/4/', Post4TemplateView.as_view(), name='post-4'),
    path('blog/post/5/', Post5TemplateView.as_view(), name='post-5'),
    path('blog/post/6/', Post6TemplateView.as_view(), name='post-6'),
]
