from django.contrib import admin

from .models import Category, Brand, ProductFeature

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
    list_display = ("product", "key", "value", "created_at", "updated_at")
    list_filter = ("product", "key", "created_at")
    search_fields = ("product", "key", "value")
    ordering = ["-created_at"]
