from django.contrib import admin

from .models import Category

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
    