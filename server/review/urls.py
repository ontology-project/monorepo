from django.conf.urls import url
from .views import ReviewListCreateView, ReviewDetailView

urlpatterns = [
    url('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    url('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]