from django.shortcuts import get_list_or_404
from django.db.models import *

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Product, WatchStatus
from .serializers import WatchStatusSerializer, ProductStatsSerializer


def get_serializer(request, queryset, product_filter=False):
    serializer_context = {'request': request}
    serializer = WatchStatusSerializer(queryset, many=True, context=serializer_context)
    return serializer


class LessonWatchStatsViewSet(viewsets.ViewSet):
    """
    Showing lesson watch stats (for user_id)
    """
    queryset = WatchStatus.objects.filter(user__products__access__blocked=0).prefetch_related('user', 'lesson')

    def list(self, request):
        queryset = get_list_or_404(self.queryset.distinct())
        serializer = get_serializer(request, queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = get_list_or_404(self.queryset.distinct())
        serializer = get_serializer(request, queryset)
        return Response(serializer.data)


def get_serializer(request, queryset):
    serializer_context = {'request': request}
    serializer = ProductStatsSerializer(queryset, many=True, context=serializer_context)
    return serializer


class ProductStatsViewSet(viewsets.ViewSet):
    """
        Showing product_stats (for product_id)
    """
    queryset = Product.objects.values('name').annotate(
        user_count=Count('users', distinct=True),
        total_watch_time=Sum('lessons__watchstatus__watch_time', distinct=True),
        watch_count=Count('lessons__watchstatus', distinct=True))

    def list(self, request):
        queryset = get_list_or_404(self.queryset)
        serializer = get_serializer(request, queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = get_list_or_404(self.queryset.filter(pk=pk))
        serializer = get_serializer(request, queryset)
        return Response(serializer.data)
