from rest_framework import serializers

from .models import Category, Item, PurchaseLink, SubCategory


class PurchaseLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseLink
        fields = ["label", "platform", "url"]


class ItemListSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(source="subcategory.name", read_only=True)
    category_slug = serializers.CharField(source="subcategory.category.slug", read_only=True)
    purchase_links = PurchaseLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            "name",
            "slug",
            "origin",
            "summary",
            "tags",
            "scene",
            "subcategory_name",
            "category_slug",
            "purchase_links",
        ]


class ItemDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="subcategory.category.name", read_only=True)
    category_slug = serializers.CharField(source="subcategory.category.slug", read_only=True)
    subcategory_name = serializers.CharField(source="subcategory.name", read_only=True)
    subcategory_slug = serializers.CharField(source="subcategory.slug", read_only=True)
    purchase_links = PurchaseLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            "name",
            "slug",
            "origin",
            "summary",
            "tags",
            "scene",
            "features",
            "pairing",
            "notes",
            "category_name",
            "category_slug",
            "subcategory_name",
            "subcategory_slug",
            "purchase_links",
        ]


class ItemSelectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="subcategory.category.name", read_only=True)
    category_slug = serializers.CharField(source="subcategory.category.slug", read_only=True)
    subcategory_name = serializers.CharField(source="subcategory.name", read_only=True)

    class Meta:
        model = Item
        fields = ["id", "name", "slug", "category_name", "category_slug", "subcategory_name"]


class SubCategorySummarySerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = SubCategory
        fields = ["name", "slug", "item_count"]


class CategoryListSerializer(serializers.ModelSerializer):
    subcategory_count = serializers.IntegerField(read_only=True)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["name", "slug", "description", "subcategory_count", "item_count"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySummarySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["name", "slug", "description", "subcategories"]
