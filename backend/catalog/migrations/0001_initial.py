from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=120, unique=True)),
                ("description", models.TextField(blank=True)),
                ("display_order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "主类",
                "verbose_name_plural": "主类",
                "ordering": ["display_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="SubCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=120)),
                ("display_order", models.PositiveIntegerField(default=0)),
                (
                    "category",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="subcategories", to="catalog.category"),
                ),
            ],
            options={
                "verbose_name": "子类",
                "verbose_name_plural": "子类",
                "ordering": ["display_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("slug", models.SlugField(max_length=140)),
                ("origin", models.CharField(blank=True, max_length=120)),
                ("summary", models.TextField(blank=True)),
                ("tags", models.JSONField(blank=True, default=list)),
                ("scene", models.TextField(blank=True)),
                ("features", models.JSONField(blank=True, default=list)),
                ("pairing", models.TextField(blank=True)),
                ("notes", models.TextField(blank=True)),
                ("display_order", models.PositiveIntegerField(default=0)),
                (
                    "subcategory",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="catalog.subcategory"),
                ),
            ],
            options={
                "verbose_name": "条目",
                "verbose_name_plural": "条目",
                "ordering": ["display_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="PurchaseLink",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(max_length=80)),
                ("platform", models.CharField(blank=True, max_length=80)),
                ("url", models.URLField(max_length=500)),
                ("display_order", models.PositiveIntegerField(default=0)),
                (
                    "item",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="purchase_links", to="catalog.item"),
                ),
            ],
            options={
                "verbose_name": "购买链接",
                "verbose_name_plural": "购买链接",
                "ordering": ["display_order", "id"],
            },
        ),
        migrations.AddConstraint(
            model_name="subcategory",
            constraint=models.UniqueConstraint(fields=("category", "slug"), name="uniq_subcategory_slug_per_category"),
        ),
        migrations.AddConstraint(
            model_name="item",
            constraint=models.UniqueConstraint(fields=("subcategory", "slug"), name="uniq_item_slug_per_subcategory"),
        ),
    ]
