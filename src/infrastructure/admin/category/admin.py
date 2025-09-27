from django.contrib import admin

class CategoryEntityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('creator', 'created_at')