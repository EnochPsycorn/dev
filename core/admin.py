from django.contrib import admin
from django.utils.html import format_html
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="200px" />'.format(obj.image.url))
    image_tag.short_description = 'Product Image Preview'
    readonly_fields = ['image_tag']
admin.site.site_header = "Shopaholic Dashboard"
admin.site.site_title = "Shopaholic"
admin.site.index_title = "Welcome to Shopaholic Dashboard"

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
# Register your models here.
