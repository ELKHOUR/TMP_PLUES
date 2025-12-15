from django.contrib import admin
from .models import Product, ProductSize, ProductMaterial, Category, ProductImage, CompanyServices, ConfirmedEmail, CompanyInfo




@admin.register(ConfirmedEmail)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'confirmed_at')
    search_fields = ('email',)
    list_filter = ('confirmed_at',)
    list_per_page = 50



# Inline لإضافة الصور داخل صفحة المنتج
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# إعدادات لوحة التحكم الخاصة بالمنتجات
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'state')
    list_filter = ('category', 'state', 'material', 'size')
    search_fields = ('name', 'description')
    filter_horizontal = ('material', 'size')
    inlines = [ProductImageInline]

# باقي الموديلات
@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')





@admin.register(CompanyServices)
class CompanyServicesAdmin(admin.ModelAdmin):
    list_display = ('ServiceName', 'ServiceDescription', 'ServiceImage')
    search_fields = ('ServiceName',)  # optional, adds search box
    list_per_page = 20  # optional, paginate results

@admin.register(CompanyInfo)
class CompanyInfo(admin.ModelAdmin):
    list_display = ('id', 'key', 'value')