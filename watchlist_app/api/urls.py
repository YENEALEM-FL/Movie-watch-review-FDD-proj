from django.urls import include, path
from rest_framework.routers import DefaultRouter

from watchlist_app.api.views import (ReviewCreate, ReviewDetail, ReviewList,
                                     StreamPlatformAV, StreamPlatformDetailAV,
                                     StreamPlatformVS, UserReview,
                                     WatchDetailAV, WatchListAV, WatchListGV)

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')


urlpatterns = [
    path('list/',WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie-detail'),
    path('list2/', WatchListGV.as_view(), name='watch-list'),

    path('', include(router.urls)),

    # path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='stream-detail'),
    # path('stream/<int:pk>/review-create', ReviewCreate.as_view(), name='review-create'),

    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail')

    path('<int:pk>/reviews/create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),

    #filtering by using username
    # path('review/<str:username>/', UserReview.as_view(), name='user-review-detail'),
    # filtering by using query param
    path('user-reviews/', UserReview.as_view(), name='user-review-detail'),
]
