from .models import Review
from .serializers import ReviewSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django.db import IntegrityError
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.permissions import AllowAny

class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_kaprodi:
            return Review.objects.all()
        return Review.objects.filter(reviewer=user)

    def perform_create(self, serializer):
        user = self.request.user
        curriculum = serializer.validated_data['curriculum']
        query = serializer.validated_data['query']
        
        # Check if a review already exists for the same curriculum and query
        if Review.objects.filter(reviewer=user, curriculum=curriculum, query=query).exists():
            raise ValidationError("You have already submitted a review for this curriculum and query.")
        
        try:
            serializer.save(reviewer=user)
        except IntegrityError:
            raise APIException("A review with this reviewer and query already exists.")

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer