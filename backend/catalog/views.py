from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Item, SubCategory
from .serializers import (
    CategoryDetailSerializer,
    CategoryListSerializer,
    ItemDetailSerializer,
    ItemListSerializer,
)


class CategoryListView(APIView):
    def get(self, request):
        queryset = Category.objects.annotate(
            subcategory_count=Count("subcategories", distinct=True),
            item_count=Count("subcategories__items", distinct=True),
        ).order_by("display_order", "id")
        serializer = CategoryListSerializer(queryset, many=True)
        return Response(serializer.data)


class CategoryDetailView(APIView):
    def get(self, request, category_slug):
        queryset = Category.objects.prefetch_related("subcategories")
        category = get_object_or_404(queryset, slug=category_slug)
        subcategories = category.subcategories.annotate(item_count=Count("items")).order_by("display_order", "id")
        serializer = CategoryDetailSerializer(category)
        data = serializer.data
        data["subcategories"] = [
            {"name": sub.name, "slug": sub.slug, "item_count": sub.item_count} for sub in subcategories
        ]
        return Response(data)


class SubCategoryItemsView(APIView):
    def get(self, request, subcategory_slug):
        subcategory = get_object_or_404(
            SubCategory.objects.select_related("category").order_by("display_order", "id"),
            slug=subcategory_slug,
        )
        items = (
            subcategory.items.select_related("subcategory", "subcategory__category")
            .prefetch_related("purchase_links")
            .order_by("display_order", "id")
        )
        serializer = ItemListSerializer(items, many=True)
        return Response(
            {
                "subcategory": {
                    "name": subcategory.name,
                    "slug": subcategory.slug,
                    "category_name": subcategory.category.name,
                    "category_slug": subcategory.category.slug,
                },
                "items": serializer.data,
            }
        )


class ItemDetailView(APIView):
    def get(self, request, item_slug):
        item = get_object_or_404(
            Item.objects.select_related("subcategory", "subcategory__category")
            .prefetch_related("purchase_links")
            .order_by("display_order", "id"),
            slug=item_slug,
        )
        serializer = ItemDetailSerializer(item)
        return Response(serializer.data)
