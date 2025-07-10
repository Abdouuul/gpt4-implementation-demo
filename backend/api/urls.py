from django.urls import path
from . import views

urlpatterns = [
    path('languages/', views.list_languages, name='list_languages'),
    path('styles/', views.list_styles, name='list_styles'),
    path('contexts/', views.list_contexts, name='list_contexts'),
    path('rewriter/', views.handle_email_rewrite, name='handle_email_rewrite'),
]