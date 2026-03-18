from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from catalog.models import Item
from .models import TastingRecord
from .serializers import TastingRecordDetailSerializer, TastingRecordListSerializer


def _set_items(record, item_ids):
    if item_ids is not None:
        ids = [int(i) for i in item_ids if i]
        record.items.set(Item.objects.filter(pk__in=ids))


class TastingRecordListView(APIView):
    def get(self, request):
        records = TastingRecord.objects.prefetch_related(
            "items", "items__subcategory", "items__subcategory__category"
        )
        serializer = TastingRecordListSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        item_ids = request.data.get("item_ids")
        serializer = TastingRecordDetailSerializer(data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            _set_items(record, item_ids)
            return Response(TastingRecordDetailSerializer(record).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TastingRecordDetailView(APIView):
    def _get_record(self, pk):
        return get_object_or_404(
            TastingRecord.objects.prefetch_related(
                "items", "items__subcategory", "items__subcategory__category"
            ),
            pk=pk,
        )

    def get(self, request, pk):
        record = self._get_record(pk)
        serializer = TastingRecordDetailSerializer(record)
        return Response(serializer.data)

    def patch(self, request, pk):
        record = self._get_record(pk)
        item_ids = request.data.get("item_ids")
        serializer = TastingRecordDetailSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            record = serializer.save()
            _set_items(record, item_ids)
            return Response(TastingRecordDetailSerializer(record).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        record = self._get_record(pk)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
