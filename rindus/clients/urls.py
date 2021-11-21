"""Clients URLs."""

# Django
from django.urls import path

# Views
from rindus.clients import views

urlpatterns = [

    path(
        route='',
        view=views.ClientsFeedView.as_view(),
        name='feed'
    ),

    path(
        route='clients/new/',
        view=views.ClientCreateView.as_view(),
        name='create'
    ),
    path(
        route='clients/<int:pk>/',
        view=views.ClientDetailView.as_view(),
        name='detail'
    ),
    path(
        route='clients/delete/<int:pk>',
        view=views.ClientDeleteView.as_view(),
        name='delete'
    ),
    path(
        route='clients/update/<int:pk>',
        view=views.ClientUpdateView.as_view(),
        name='update'
    ),
]