from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import mixins
from rest_framework import filters, generics, status, viewsets
# from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.throttling import (AnonRateThrottle, ScopedRateThrottle,
                                       UserRateThrottle)
from rest_framework.views import APIView

from watchlist_app.api.pagination import (WatchListCPagination,
                                          WatchListLOPagination,
                                          WatchListPagination)
from watchlist_app.api.permissions import (IsAdminOrReadOnly,
                                           IsReviewUserOrReadOnly)
from watchlist_app.api.serializers import (ReviewSerializer,
                                           StreamPlatformSerializer,
                                           WatchListSerializer)
from watchlist_app.api.throttling import (ReviewCreateThrottle,
                                          ReviewListThrottle)
from watchlist_app.models import Review, StreamPlatform, WatchList


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

# #using a referential field, or foreignkey use __

#     def get_queryset(self):
#         username = self.kwargs['username']
#         return Review.objects.filter(review_user__username=username)

# using queryp arameter
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    throttle_scope = ['review-detail']
    # filter_backends = [DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    # filterset_fields = ['review_user__username', 'active']
    search_fields = ['review_user__username', 'active']


    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly] object level permission
    # permission_classes = [AdminOrReadOnly] Admin or User only privilege
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'



# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]

# class StreamPlatformVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

class StreamPlatformAV(APIView):

    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True,  context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'stream platform not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'StreamPlatform not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# watchlist for filter
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # pagination_class = WatchListPagination
    # pagination_class = WatchListLOPagination

    pagination_class = WatchListCPagination

    # watchlist for searching
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['^title', 'platform__name']

    # watchlist for ordering
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']

    # - comment this our for Cursor pagination practice
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']



class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        watchLists = WatchList.objects.all()
        serializer = WatchListSerializer(watchLists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            watchList = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(watchList)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            watchList = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(watchList, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        watchList = WatchList.objects.get(pk=pk)
        watchList.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# # @api_view(['GET', 'POST'])
# # def watchListWatchList_list(request):

# #     if request.method == 'GET':
# #         watchListWatchLists =WatchList.objects.all()
# #         serializer =WatchListSerializer(watchListWatchLists, many=True)
# #         return Response(serializer.data)

# #     if request.method == 'POST':
# #         serializer =WatchListSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         else:
# #             return Response(serializer.errors)

# # @api_view(['GET', 'PUT', 'DELETE'])
# # def watchListWatchList_details(request, pk):
# #     if request.method == 'GET':
# #         try:
# #             watchListWatchList =WatchList.objects.get(pk=pk)
# #         exceptWatchList.DoesNotExist:
# #             return Response({'error':'WatchListWatchList not found'}, status=status.HTTP_404_NOT_FOUND)

# #         serializer =WatchListSerializer(watchListWatchList)
# #         return Response(serializer.data)

# #     if request.method == 'PUT':
# #         watchListWatchList =WatchList.objects.get(pk=pk)
# #         serializer =WatchListSerializer(watchListWatchList, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         else:
# #             return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

# #     if request.method == 'DELETE':
# #         watchListWatchList =WatchList.objects.get(pk=pk)
# #         watchListWatchList.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
