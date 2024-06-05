from django.conf.urls import url
from .views import ReviewListCreateView, ReviewDetailView

urlpatterns = [
    url(r'^$', ReviewListCreateView.as_view(), name='review-list-create'),
    url(r'^(?P<pk>\d+)/$', ReviewDetailView.as_view(), name='review-detail'),
]
