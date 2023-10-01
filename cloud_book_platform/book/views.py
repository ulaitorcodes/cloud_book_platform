from rest_framework import viewsets, response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework .views import APIView
from django.shortcuts import get_object_or_404
from cloud_book_platform.book.models import (Book, 
                                             BookSection)

from cloud_book_platform.book.serializers import (BookSerializer, 
                                                  BookSectionSerializer,
                                                  RecursiveBookSectionSerializer
                                                  )

from cloud_book_platform.book.permissions import IsAuthor, IsCollaborator, IsAuthorOrReadOnly, IsAuthorOrCollaborator

from django.contrib.auth import get_user_model
User = get_user_model()


# Book creation view
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Retrieve the author from the authenticated user
        author = self.request.user
        # Setting the author fiueld in the serializer
        serializer.save(author=author)
    
    def retrieve(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        sections = BookSection.objects.filter(book=book)
        serialized_data = self.get_serializer(book).data
        serialized_data['sections'] = BookSectionSerializer(sections, many=True).data
        return response.Response(serialized_data)
    
    def perform_update(self, serializer):
        author = self.request.user

        # Ensure the author is the owner of the section or subsection

        if author == serializer.instance.author:
            serializer.save()
        else:
            return response.Response(
                {"error":"Unathourized"},
                status=status.HTTP_403_FORBIDDEN
            )


class BookSectionViewSet(viewsets.ModelViewSet):
    queryset = BookSection.objects.all()
    serializer_class = BookSectionSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrCollaborator]


  
    def perform_create(self, serializer):
        try:
            book_id = self.kwargs.get('book_pk')
            book = Book.objects.get(id=book_id)
            

            if book.author == self.request.user:
                serializer.save(book=book)
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return response.Response({"detail": "You do not have the permission to create a section for this book"})
        except Book.DoesNotExist:
            return response.Response({"detail": "Book matching query does not exist"},
                                     status=status.HTTP_404_NOT_FOUND)
    
    def retrieve(self, request, pk=None):
        try:
            parent_section = BookSection.objects.get(pk=pk)
        except BookSection.DoesNotExist:
            return response.Response({"error": "Section nor found"}, status=404)
        
        subsections = BookSection.objects.filter(parent_section=parent_section)
        serialized_data = RecursiveBookSectionSerializer(subsections, many=True).data
        return response.Response(serialized_data)
    

# Add / Revoke Collaborators

class BookCollaboratorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            book = Book.objects.get(id=pk)

            if book.author == self.request.user:
                collaborators = request.data.get('collaborators', [])
                users = User.objects.filter(email__in=collaborators)
                book.collaborators.add(*users)
                return response.Response({"details":"Collaborators added successfully"}, status=status.HTTP_200_OK)
            
            else:
                return response.Response({"detail":"Only the Author can manage collaborators for this book"}, status=status.HTTP_403_FORBIDDEN)
            
        except Book.DoesNotExist:
            return response.Response({"detail" : "Book matching query does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            
            if book.author == self.request.user:
                collaborators = request.data.get('collaborators', [])
                users = User.objects.filter(email__in=collaborators)
                book.collaborators.remove(*users)
                return response.Response({"detail":"collaborator removed successfully"}, status=status.HTTP_200_OK)            
            else:
                return response.Response({"detail":"only the Author can manage collaborators for this book"}, status=status.HTTP_403_FORBIDDEN)
            
        except Book.DoesNotExist:
            return response.Response({"detail":"Book matching query does not exist"}, status=status.HTTP_404_NOT_FOUND)

