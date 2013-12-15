from django.contrib import admin

# Register your models here.
from django.contrib import admin
from books.models import Book, Category, Role, Collaboration

# This is so the admin automatically suggests slugs,
# based on the title:

class CollaborationInline(admin.TabularInline):
    model = Collaboration
    extra = 1

class BookAdmin(admin.ModelAdmin):
    inlines = (CollaborationInline,)
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class RoleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Book, BookAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Collaboration)
