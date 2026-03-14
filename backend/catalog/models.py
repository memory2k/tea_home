from django.db import models


class Category(models.Model):
    name = models.CharField("名称", max_length=100)
    slug = models.SlugField("标识", unique=True, max_length=120)
    description = models.TextField("说明", blank=True)
    display_order = models.PositiveIntegerField("显示顺序", default=0)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "主类"
        verbose_name_plural = "主类"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name="主类",
        on_delete=models.CASCADE,
        related_name="subcategories",
    )
    name = models.CharField("名称", max_length=100)
    slug = models.SlugField("标识", max_length=120)
    display_order = models.PositiveIntegerField("显示顺序", default=0)

    class Meta:
        ordering = ["display_order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["category", "slug"], name="uniq_subcategory_slug_per_category")
        ]
        verbose_name = "子类"
        verbose_name_plural = "子类"

    def __str__(self):
        return f"{self.category.name} / {self.name}"


class Item(models.Model):
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name="子类",
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.CharField("名称", max_length=120)
    slug = models.SlugField("标识", max_length=140)
    origin = models.CharField("来源", max_length=120, blank=True)
    summary = models.TextField("摘要", blank=True)
    tags = models.JSONField("关键词", default=list, blank=True)
    scene = models.TextField("适用场景", blank=True)
    features = models.JSONField("核心特征", default=list, blank=True)
    pairing = models.TextField("适配建议", blank=True)
    notes = models.TextField("备注", blank=True)
    display_order = models.PositiveIntegerField("显示顺序", default=0)

    class Meta:
        ordering = ["display_order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["subcategory", "slug"], name="uniq_item_slug_per_subcategory")
        ]
        verbose_name = "条目"
        verbose_name_plural = "条目"

    def __str__(self):
        return self.name


class PurchaseLink(models.Model):
    item = models.ForeignKey(Item, verbose_name="条目", on_delete=models.CASCADE, related_name="purchase_links")
    label = models.CharField("链接名称", max_length=80)
    platform = models.CharField("平台", max_length=80, blank=True)
    url = models.URLField("链接地址", max_length=500)
    display_order = models.PositiveIntegerField("显示顺序", default=0)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "购买链接"
        verbose_name_plural = "购买链接"

    def __str__(self):
        return f"{self.item.name} / {self.label}"
