from django.contrib import admin
from django.utils.translation import gettext_lazy

from datetime import datetime, timedelta

from .models import Category, Brand, ProductFeature, Product, ProductImage


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductFeatureInline(admin.StackedInline):
    model = ProductFeature


class CustomDateFilter(admin.SimpleListFilter):
    title = gettext_lazy("Created data")
    parameter_name = "created_at"
    
    def lookups(self, request, model_admin):
        return [
            ("today", gettext_lazy("Today")),
            ("past_7_days", gettext_lazy("Past 7 Days")),
            ("this_month", gettext_lazy("This Month")),
            ("this_year", gettext_lazy("This Year")),
        ]
        
    def queryset(self, request, queryset):
        value = self.value()
        today = datetime.now().date()
        
        if value == "today":
            return queryset.filter(created_at__date=today)
        elif value == "past_7_days":
            return queryset.filter(created_at__date__gte=today - timedelta(days=7))
        elif value == "this_month":
            return queryset.filter(created_at__year=today.year, created_at__month=today.month)
        elif value == "this_year":
            return queryset.filter(created_at__year=today.year)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ("parent", "name", "image")
    
    def image_preview(self, obj):
        if obj.image:
            return f"<img src='{obj.image.url}' \
                style='with= 50px; height=auto;'>"
        return "No image"
    
    # the method's output contains HTML
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"
    

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "image", )
    search_fields = ("name", )
    ordering = ("name", )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "price", "quantity", "active", "created_at")
    search_fields = ("name", )
    list_filter = ("category", "brand", "active", CustomDateFilter)
    ordering = ("name",)
    inlines = [ProductFeatureInline, ImageInline]
