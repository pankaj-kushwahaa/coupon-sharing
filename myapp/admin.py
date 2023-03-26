from django.contrib import admin
from .models import Company, Coupon, Category, UserProfile

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['name','image', 'id']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
  list_display = ['name','category', 'id']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
  list_display = ['title', 'description', 'code', 'company','category', 'added_by', 
  'collected_by', 'validity', 'used']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
  list_display = ['user', 'dp', 'credits']

