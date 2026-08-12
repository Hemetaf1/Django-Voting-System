from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sections/', views.sections_htmx, name='sections_htmx'),
    # Voting endpoints
    path('vote/<int:project_id>/', views.vote_view, name='vote'),
    path('vote-count/<int:project_id>/', views.vote_count, name='vote_count'),
    path('feedback/', views.feedback_api, name='feedback'),
    path('export/', views.export_xlsx, name='export_xlsx'),
    path('qr/', views.qrcode_view, name='qrcode'),
    # Subcategory page view
    path(
        'subcategory/<str:cat_value>/<slug:sub_slug>/',
        views.subcategory_view,
        name='subcategory'
    ),
] 