import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import Category, Item, PurchaseLink, SubCategory


class Command(BaseCommand):
    help = "Import tea library data from the original JSON file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default=str(Path(__file__).resolve().parents[4] / "frontend" / "public" / "data" / "tea-library.json"),
            help="Path to the source JSON file.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        source_path = Path(options["path"])
        if not source_path.exists():
            raise CommandError(f"JSON file not found: {source_path}")

        payload = json.loads(source_path.read_text(encoding="utf-8"))

        PurchaseLink.objects.all().delete()
        Item.objects.all().delete()
        SubCategory.objects.all().delete()
        Category.objects.all().delete()

        for category_index, raw_category in enumerate(payload.get("categories", [])):
            category = Category.objects.create(
                name=raw_category["name"],
                slug=raw_category["id"],
                description=raw_category.get("description", ""),
                display_order=category_index,
            )

            subcategory_map = {}
            for sub_index, raw_subcategory in enumerate(raw_category.get("subcategories", [])):
                subcategory = SubCategory.objects.create(
                    category=category,
                    name=raw_subcategory["name"],
                    slug=raw_subcategory["id"],
                    display_order=sub_index,
                )
                subcategory_map[raw_subcategory["id"]] = subcategory

            for item_index, raw_item in enumerate(raw_category.get("items", [])):
                subcategory = subcategory_map.get(raw_item["subcategoryId"])
                if not subcategory:
                    raise CommandError(
                        f"Missing subcategory '{raw_item['subcategoryId']}' for item '{raw_item['id']}'"
                    )

                item = Item.objects.create(
                    subcategory=subcategory,
                    name=raw_item["name"],
                    slug=raw_item["id"],
                    origin=raw_item.get("origin", ""),
                    summary=raw_item.get("summary", ""),
                    tags=raw_item.get("tags", []),
                    scene=raw_item.get("scene", ""),
                    features=raw_item.get("features", []),
                    pairing=raw_item.get("pairing", ""),
                    notes=raw_item.get("notes", ""),
                    display_order=item_index,
                )

                for link_index, raw_link in enumerate(raw_item.get("purchaseLinks", [])):
                    PurchaseLink.objects.create(
                        item=item,
                        label=raw_link["label"],
                        platform=raw_link.get("platform", ""),
                        url=raw_link["url"],
                        display_order=link_index,
                    )

        self.stdout.write(self.style.SUCCESS("Tea library imported successfully."))
