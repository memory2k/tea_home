from rest_framework import serializers

from catalog.models import Item
from .models import TastingRecord


class TastingItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="subcategory.category.name", read_only=True)
    category_slug = serializers.CharField(source="subcategory.category.slug", read_only=True)
    subcategory_name = serializers.CharField(source="subcategory.name", read_only=True)

    class Meta:
        model = Item
        fields = ["id", "name", "slug", "category_name", "category_slug", "subcategory_name"]


class TastingRecordListSerializer(serializers.ModelSerializer):
    items = TastingItemSerializer(many=True, read_only=True)

    class Meta:
        model = TastingRecord
        fields = [
            "id",
            "date",
            "items",
            "rating",
            "color",
            "taste",
            "location",
            "participants",
        ]


class TastingRecordDetailSerializer(serializers.ModelSerializer):
    items = TastingItemSerializer(many=True, read_only=True)

    class Meta:
        model = TastingRecord
        fields = [
            "id",
            "date",
            "items",
            "water_temp",
            "steep_time",
            "tea_amount",
            "water_type",
            "aroma",
            "taste",
            "color",
            "rating",
            "notes",
            "weather",
            "location",
            "participants",
            "created_at",
            "updated_at",
        ]
