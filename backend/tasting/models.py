from django.db import models
from django.utils.timezone import now

from catalog.models import Item


class TastingRecord(models.Model):
    # 基本信息
    date = models.DateTimeField("品茗时间", default=now)
    items = models.ManyToManyField(
        Item,
        verbose_name="品茗条目",
        blank=True,
        related_name="tasting_records",
    )

    # 冲泡参数
    water_temp = models.PositiveSmallIntegerField("水温（℃）", null=True, blank=True)
    steep_time = models.PositiveSmallIntegerField("浸泡时长（秒）", null=True, blank=True)
    tea_amount = models.CharField("用茶量", max_length=40, blank=True)
    water_type = models.CharField("用水", max_length=80, blank=True)

    # 品评
    aroma = models.TextField("香气", blank=True)
    taste = models.TextField("口感", blank=True)
    color = models.CharField("汤色", max_length=60, blank=True)
    rating = models.PositiveSmallIntegerField("评分", null=True, blank=True)

    # 附记
    notes = models.TextField("备注", blank=True)
    weather = models.CharField("天气", max_length=60, blank=True)
    location = models.CharField("地点", max_length=120, blank=True)
    participants = models.TextField("参与人", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "品茗记录"
        verbose_name_plural = "品茗记录"

    def __str__(self):
        names = "、".join(self.items.values_list("name", flat=True)[:3])
        return f"{self.date.strftime('%Y-%m-%d')} · {names or '（无条目）'}"
