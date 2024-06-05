from .models import Review
from .serializers import ReviewSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django.db import IntegrityError
from rest_framework.exceptions import APIException

class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(reviewer__username=username)
        return queryset

    def perform_create(self, serializer):
        try:
            serializer.save(reviewer=self.request.user)
        except IntegrityError:
            raise APIException("A review with this reviewer and query already exists.")

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer