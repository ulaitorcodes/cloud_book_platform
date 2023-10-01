from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):

    """
        This is a custom permission class to allow Authors edit their own sections and subsections.
    """

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author == request.user


class IsAuthor(permissions.BasePermission):

    def has_permission(self, request, view):

        # Allow section creation [POST]  only if the user is the Author

        if view.action == 'create':
            author_id = view.kwargs.get('author_pk')
            return request.user.is_authenticated and request.user.id == author_id
        return True
            
    
class IsCollaborator(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):

        return(
            request.user.is_authenticated and
            request.user in obj.book.collaborators.all() and
            view.action in ['retrieve', 'update', 'partial_update']
        )



class IsAuthorOrCollaborator(permissions.BasePermission):

    def has_permission(self, request, view):

        # Allow section editing (POST) for Author only
        if view.action == 'create':
            return request.user.is_authenticated
        return True
      
    
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update']:
            return (
                request.user.is_authenticated and
                (request.user == obj.book.author or 
                 (request.user in obj.book.collaborators.all()))
            )
        return True
      
        

