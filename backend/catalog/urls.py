from django.urls import path

from .views import CategoryDetailView, CategoryListView, ItemDetailView, SubCategoryItemsView


urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="api-categories"),
    path("categories/<slug:category_slug>/", CategoryDetailView.as_view(), name="api-category-detail"),
    path("subcategories/<slug:subcategory_slug>/items/", SubCategoryItemsView.as_view(), name="api-subcategory-items"),
    path("items/<slug:item_slug>/", ItemDetailView.as_view(), name="api-item-detail"),
]
