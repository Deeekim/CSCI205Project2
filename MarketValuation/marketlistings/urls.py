from django.urls import path
from . import views

app_name = 'marketlistings'
urlpatterns = [

    # http://localhost:8000/marketlistings/home/
    path('home/', views.home, name='home'),

    # http://localhost:8000/marketlistings/upload-csv/
    path('upload-csv/', views.upload_csv, name='upload_csv'),

    # http://localhost:8000/marketlistings/view/all/
    path('view/all/', views.viewall, name='view-all'),

    # http://localhost:8000/marketlistings/new/
    path('new/', views.addlistings, name='add_listing'),

    # http://localhost:8000/marketlistings/view/1/
    path('view/<int:pk>/', views.view_listing, name='view_listing'),

    # http://localhost:8000/marketlistings/edit/1/
    path('edit/<int:pk>/', views.edit_listing, name='edit_listing'),

    # http://localhost:8000/marketlistings/delete/1/
    path('delete/<int:pk>/', views.delete_listing, name='delete_listing'),

]