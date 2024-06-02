from .models import Review
from .serializers import ReviewSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

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
        serializer.save(reviewer=self.request.user)

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer