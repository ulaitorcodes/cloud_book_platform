from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cloud_book_platform.book.views import (BookViewSet, 
                                            BookSectionViewSet,
                                            )


book_list = BookViewSet.as_view({'get': 'list','post': 'create'})
book_detail = BookViewSet.as_view({'get': 'retrieve'})

book_section_list = BookSectionViewSet.as_view({'get': 'list','post': 'create'})
book_section_detail = BookSectionViewSet.as_view({'get': 'retrieve'})

book_section_update = BookSectionViewSet.as_view({'put': 'update'})

urlpatterns = [
    path('', book_list, name='book_viewset'),
    path('<int:pk>/', book_detail, name='book_viewset'),

    # Book section urls
    path('section/', book_section_list, name='book_section_viewset'),
    path('section/<int:pk>/', book_section_detail, name='book_section_detail_viewset'),

    path('section/<int:pk>/update/', book_section_update, name='book_section_update_viewset'),

]