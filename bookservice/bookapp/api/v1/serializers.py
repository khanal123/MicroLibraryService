from rest_framework import serializers
from bookapp.models import book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = book
        fields = "__all__"