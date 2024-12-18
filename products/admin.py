from django.contrib import admin

from .models import Category, Brand, ProductFeature, Product

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
    list_display = ("product", "key", "value")
    list_filter = ("product", "key", )
    search_fields = ("product", "key", "value")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "price", "quantity", "active")
    search_fields = ("name", "active")
    list_filter = ("category", "brand", "active")
    ordering = ("name",)
     