from .models import Review
from .serializers import ReviewSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django.db import IntegrityError
from rest_framework.exceptions import APIException
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
        try:
            serializer.save(reviewer=self.request.user)
        except IntegrityError:
            raise APIException("A review with this reviewer and query already exists.")

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer