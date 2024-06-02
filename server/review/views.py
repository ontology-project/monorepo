from .models import Review
from .serializers import ReviewSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
