from django.conf.urls import url
from .views import ReviewListCreateView, ReviewDetailView

urlpatterns = [
    url('', ReviewListCreateView.as_view(), name='review-list-create'),
    url('/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]