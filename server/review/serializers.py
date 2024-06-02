from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.ReadOnlyField(source='reviewer.username')

    class Meta:
        model = Review
        fields = ['id', 'created_at', 'updated_at', 'comment', 'rating', 'reviewer', 'query', 'curriculum']