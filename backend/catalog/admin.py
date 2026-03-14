from django.contrib import admin

from .models import Category, Item, PurchaseLink, SubCategory


class PurchaseLinkInline(admin.TabularInline):
    model = PurchaseLink
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "display_order")
    search_fields = ("name", "slug")
    ordering = ("display_order", "id")


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug", "display_order")
    list_filter = ("category",)
    search_fields = ("name", "slug", "category__name")
    ordering = ("category", "display_order", "id")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "subcategory", "slug", "origin", "display_order")
    list_filter = ("subcategory__category", "subcategory")
    search_fields = ("name", "slug", "origin")
    ordering = ("subcategory", "display_order", "id")
    inlines = [PurchaseLinkInline]


@admin.register(PurchaseLink)
class PurchaseLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "platform", "item", "display_order")
    list_filter = ("platform", "item__subcategory__category")
    search_fields = ("label", "platform", "item__name")
