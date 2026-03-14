from django.test import TestCase
from django.urls import reverse

from .models import Category, Item, PurchaseLink, SubCategory


class CatalogModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="茶具", slug="tea-ware", description="desc", display_order=0)
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name="茶盘",
            slug="tea-tray",
            display_order=0,
        )
        self.item = Item.objects.create(
            subcategory=self.subcategory,
            name="竹制干泡茶盘",
            slug="bamboo-tray",
            origin="福建",
            tags=["竹材"],
            features=["导水顺畅"],
        )
        self.link = PurchaseLink.objects.create(
            item=self.item,
            label="淘宝购买",
            platform="淘宝",
            url="https://example.com",
        )

    def test_cascade_delete_category(self):
        self.category.delete()
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(SubCategory.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(PurchaseLink.objects.count(), 0)


class CatalogApiTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="茶具", slug="tea-ware", description="desc", display_order=0)
        subcategory = SubCategory.objects.create(category=category, name="茶盘", slug="tea-tray", display_order=0)
        item = Item.objects.create(
            subcategory=subcategory,
            name="竹制干泡茶盘",
            slug="bamboo-tray",
            origin="福建",
            summary="summary",
            tags=["竹材"],
            scene="scene",
            features=["导水顺畅"],
            pairing="pairing",
            notes="notes",
        )
        PurchaseLink.objects.create(item=item, label="淘宝购买", platform="淘宝", url="https://example.com")

    def test_category_list(self):
        response = self.client.get(reverse("api-categories"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["slug"], "tea-ware")

    def test_category_detail(self):
        response = self.client.get(reverse("api-category-detail", args=["tea-ware"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["subcategories"][0]["slug"], "tea-tray")

    def test_subcategory_items(self):
        response = self.client.get(reverse("api-subcategory-items", args=["tea-tray"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["items"][0]["slug"], "bamboo-tray")

    def test_item_detail(self):
        response = self.client.get(reverse("api-item-detail", args=["bamboo-tray"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["purchase_links"][0]["label"], "淘宝购买")

    def test_not_found(self):
        response = self.client.get(reverse("api-item-detail", args=["missing"]))
        self.assertEqual(response.status_code, 404)
