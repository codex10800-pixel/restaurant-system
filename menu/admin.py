from django.contrib import admin
from .models import Category, MenuItem, Reservation


# =========================
# CATEGORY ADMIN
# =========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)
    list_editable = ('order',)
    ordering = ('order',)


# =========================
# MENU ITEM ADMIN (PREMIUM)
# =========================

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'available',
        'featured',
        'created_at'
    )

    list_filter = ('category', 'available', 'featured')
    search_fields = ('name', 'description')
    list_editable = ('price', 'available', 'featured')

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "description", "category")
        }),
        ("Pricing & Image", {
            "fields": ("price", "image")
        }),
        ("Status", {
            "fields": ("available", "featured")
        }),
    )

    readonly_fields = ('created_at',)


# =========================
# RESERVATION ADMIN
# =========================

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'guests', 'phone', 'email')
    list_filter = ('date', 'time')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-date',)
