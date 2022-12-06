from django.contrib import admin
from .models import Product, Category, Client, Order

# Register your models here.

# ****** Question 1 *****
# In admin.py create a class ProductAdmin(admin.ModelAdmin), register this with the admin site
# and show the name, category, price, stock, and available fields, for each Product, in the admin
# interface page that lists all Products


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    actions = ['add_stock']
    fields = ['stock']

    # ***** Question 3 *********
    @admin.action(description='Add 50 to stock')
    def add_stock(self, request, queryset):
        for product in queryset:
            product.stock = product.stock + 50
            product.save()

        self.message_user(request, message='Successfully added')


# ***** Question 2 *****
# In admin.py create a class ClientAdmin(admin.ModelAdmin), register this with the admin site
# and show the first_name, last_name, city fields and list of categories the client is interested in,
# for each client, in the admin interface page that lists all clients


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'interested_categories')

    def interested_categories(self, obj):
        return "\n".join([i.name for i in obj.interested_in.all()])


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order)
