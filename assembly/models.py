from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True, default='')
    website = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class Part(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='parts'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name='parts'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    specs = models.JSONField()
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['category', 'price'],
                name='part_category_price_idx',
            ),
        ]

    def __str__(self):
        return self.title


class Review(models.Model):
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.part.title} - {self.author.username} ({self.rating})'


class Build(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='builds'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_tdp = models.PositiveIntegerField(default=0)
    recommended_psu_watts = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=False)
    share_token = models.CharField(max_length=64, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['author', '-created_at'],
                name='build_author_date_idx',
            ),
        ]

    def __str__(self):
        return f'{self.title} ({self.author.username})'


class BuildItem(models.Model):
    build = models.ForeignKey(
        Build,
        on_delete=models.CASCADE,
        related_name='items'
    )
    part = models.ForeignKey(
        Part,
        on_delete=models.PROTECT,
        related_name='build_items'
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.build.title}: {self.part.title} x{self.quantity}'
