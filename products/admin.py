from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta

from .models import Category, Brand, ProductFeature, Product, ProductImage


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductFeatureInline(admin.StackedInline):
    model = ProductFeature


class CustomDateFilter(admin.SimpleListFilter):
    title = _('Created Date')  # عنوان فیلتر در پنل ادمین
    parameter_name = 'created_at'  # پارامتر URL برای فیلتر

    def lookups(self, request, model_admin):
        """تعریف گزینه‌های نمایش در فیلتر"""
        return [
            ('today', _('Today')),                # امروز
            ('past_7_days', _('Past 7 Days')),    # 7 روز گذشته
            ('this_month', _('This Month')),      # ماه جاری
            ('this_year', _('This Year')),        # سال جاری
        ]

    def queryset(self, request, queryset):
        """منطق فیلترها"""
        value = self.value()
        today = datetime.now().date()

        if value == 'today':
            return queryset.filter(created_at__date=today)
        elif value == 'past_7_days':
            return queryset.filter(created_at__date__gte=today - timedelta(days=7))
        elif value == 'this_month':
            return queryset.filter(created_at__year=today.year, created_at__month=today.month)
        elif value == 'this_year':
            return queryset.filter(created_at__year=today.year)
        return queryset


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


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ("product",)
    list_filter = ("product", )
    
    search_fields = ("product",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "price", "quantity", "active")
    search_fields = ("name", )
    list_filter = ("category", "brand", "active", CustomDateFilter)
    ordering = ("name",)
    inlines = (ImageInline, ProductFeatureInline)
