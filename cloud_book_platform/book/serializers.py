from rest_framework import serializers
from cloud_book_platform.book.models import Book, BookSection
from django.contrib.auth import get_user_model
User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('author',)


        # Sill making sure the 'Author' field is required
        author = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all(), 
            required=True
        )

        def create(self, validated_data):

            # retrieve the current loggedin user
            user = self.context['request'].user

            # Added the user as the Author
            validated_data['author'] = user

            # create and return the book
            book = Book.objects.create(**validated_data)
            return book

class BookSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSection
        fields = ['id', 'title', 'content', 'book', 'parent_section']

        def get_children(self, obj):
            children = BookSection.objects.filter(parent_section=obj.id)
            serializer = self.__class__(children, many=True)

            return serializer.data
            

        def validate(self, data):
            parent_section = data.get('parent_section')
            
            try:
                parent_section = BookSection.objects.get(pk=parent_section.pk)
            except BookSection.DoesNotExist:
                raise serializers.ValidationError("The specidied Parent section does not exist!")
            
            return data
        
        

class RecursiveBookSectionSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    class Meta:
        model = BookSection
        fields = ['id', 'title', 'content', 'children']

    def get_children(self, obj):
        children = BookSection.objects.filter(parent_section=obj.id)
        serializer = self.__class__(children, many=True)
        return RecursiveBookSectionSerializer(children, many=True).data
    