from django.contrib import admin
from .models import Like,Category,Video,Logo
admin.site.register(Like)

@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('show_img',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'get_categories','slug', 'parent','status')
    list_filter = ['status']
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Video)
class HomeAdmin(admin.ModelAdmin):
    list_display=('title', 'show_img','slug', 'auther', 'jpublish', 'status', 'category_to_str')
    list_filter = ('publish','status', 'auther')
    search_fields = ('title', 'description')
    prepopulated_fields= {'slug':('title',)}
    
