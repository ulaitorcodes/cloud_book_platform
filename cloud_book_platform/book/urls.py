from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cloud_book_platform.book.views import (BookViewSet, 
                                            BookSectionViewSet,
                                            BookCollaboratorAPIView
                                            )


book_list = BookViewSet.as_view({'get': 'list','post': 'create'})
book_detail = BookViewSet.as_view({'get': 'retrieve'})
book_manage_collaborators = BookCollaboratorAPIView.as_view()


book_section_list = BookSectionViewSet.as_view({'get': 'list','post': 'create'})
book_section_detail = BookSectionViewSet.as_view({'get': 'retrieve'})

book_section_update = BookSectionViewSet.as_view({'put': 'update'})

urlpatterns = [

    # List and create Books
    path('', book_list, name='book_viewset'),

    # Retrieve Books
    path('<int:pk>/', book_detail, name='book_viewset'),

    # Add and remove collaboarators
    path('<int:pk>/collaborators/', book_manage_collaborators, name='book_manage_collaborators'),

    # Book section urls
    path('section/', book_section_list, name='book_section_viewset'),
    path('section/<int:pk>/', book_section_detail, name='book_section_detail_viewset'),

    path('section/<int:pk>/update/', book_section_update, name='book_section_update_viewset'),


]