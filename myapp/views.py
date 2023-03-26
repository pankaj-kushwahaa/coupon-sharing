from django.shortcuts import render, redirect
from .forms import CouponForm
from django.views import View
from django.contrib import messages
from .models import UserProfile
from .forms import (Category, Company, Coupon,  CouponForm, CustomerRegistrationForm, CompanyForm, CategoryForm, UserProfileForm, UserProfileForm2)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from pprint import pprint
from django.views.generic import DetailView
from django.db.models import Count, F
from datetime import date
import os
from django.db import connection 
from django.db.models import Q
 
def custom_sql(sql, values): 
    with connection.cursor() as cursor: 
        cursor.execute(sql, values)
        row = cursor.fetchall() 
    return row

# Create your views here.
class Home(View):
  def get(self, request):
    ct = Category.objects.prefetch_related('category_coupon')
    # print(f'\n\n{ct}\n')
    # print(f'{ct.query}\n')
    cp = Coupon.objects.filter(collected_by=None, validity__gt=date.today()).order_by('-id')
    return render(request, 'myapp/index.html', dict(ct=ct, cp=cp))


class CustomerRegistration(View):
  def get(self, request):
    form = CustomerRegistrationForm(label_suffix=" ")
    return render(request, 'myapp/customerregistration.html', dict(form=form))
  def post(self, request):
    form = CustomerRegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Congratulations!! Registered Successfully')
      # form = CustomerRegistration(label_suffix=" ")
    return render(request, 'myapp/customerregistration.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
    profiledetail = UserProfile.objects.filter(user_id=request.user.id)
    cp = Coupon.objects.filter(collected_by=request.user)
    data = dict(profiledetail=profiledetail, cp=cp)
    return render(request, 'myapp/profile.html', data)

@method_decorator(login_required, name='dispatch')
class AddCoupon(View):
  def get(self, request):
    fm = CouponForm()
    profiledetail = UserProfile.objects.filter(user_id=request.user.id)
    data = dict(forms=fm, profiledetail=profiledetail)
    return render(request, 'myapp/add_coupon.html', data)

  def post(self, request):
    fm = CouponForm(request.POST, request.FILES)
    if fm.is_valid():
      added_by = request.user
      title = fm.cleaned_data['title']
      desc = fm.cleaned_data['description']
      code = fm.cleaned_data['code']
      company = fm.cleaned_data['company']
      category = fm.cleaned_data['category']
      validity = fm.cleaned_data['validity']
      image = fm.cleaned_data['image']
      reg = Coupon(title=title, description=desc, code=code, company=company, category=category, validity=validity, added_by=added_by, image=image)
      reg.save()
      messages.success(request, "Coupon Added Successfully")
      profiledetail = UserProfile.objects.filter(user_id=request.user.id)
      profiledetail.update(credits=F('credits') + 1)
      profiledetail = UserProfile.objects.filter(user_id=request.user.id)
      fm = CouponForm()
      data = dict(forms=fm, profiledetail=profiledetail)
      return render(request, 'myapp/add_coupon.html', data)
    else:
      fm = CouponForm(request.POST)
      profiledetail = UserProfile.objects.filter(user_id=request.user.id)
      data = dict(forms=fm, profiledetail=profiledetail)
      return render(request, 'myapp/add_coupon.html', data)

@method_decorator(login_required, name='dispatch')
class AddCompany(View):
  def get(self, request):
    fm = CompanyForm()
    profiledetail = UserProfile.objects.filter(user_id=request.user.id)
    data = dict(forms=fm, profiledetail=profiledetail)
    return render(request, 'myapp/add_company.html', data)

  def post(self, request):
    fm = CompanyForm(request.POST)
    if fm.is_valid():
      fm.save()
      messages.success(request, "Company Added")
      fm = CompanyForm()
      profiledetail = UserProfile.objects.filter(user_id=request.user.id)
      data = dict(forms=fm, profiledetail=profiledetail)
      return render(request, 'myapp/add_company.html', data)
    else:
      fm = CompanyForm(request.POST)
      profiledetail = UserProfile.objects.filter(user_id=request.user.id)
      data = dict(forms=fm, profiledetail=profiledetail)
      return render(request, 'myapp/add_company.html', data)

@method_decorator(login_required, name='dispatch')
class AddCategory(View):
  def get(self, request):
    fm = CategoryForm()
    profiledetail = UserProfile.objects.filter(user_id=request.user.id)
    data = dict(forms=fm, profiledetail=profiledetail)
    return render(request, 'myapp/add_category.html', data)

  def post(self, request):
    fm = CategoryForm(request.POST, request.FILES)
    if fm.is_valid():
      fm.save()
      messages.success(request, "Category Added Successfully")
      fm = CategoryForm()
      profiledetail = UserProfile.objects.filter(user_id=request.user.id)
      data = dict(forms=fm, profiledetail=profiledetail)
      return render(request, 'myapp/add_category.html', data)
    else:
      fm = CategoryForm(request.POST)
      profiledetail = UserProfile.objects.filter(user_id=request.user.id)
      data = dict(forms=fm, profiledetail=profiledetail)
      return render(request, 'myapp/add_category.html', data)


class CategoryShow(View):
  def get(self, request, pk):
    if pk:
      cm = Company.objects.filter(category=pk)
      cp = Coupon.objects.filter(category=pk, collected_by=None, validity__gt=date.today())
    else:
      cm = Company.objects.all()
      cp = Coupon.objects.filter(collected_by=None, validity__gt=date.today())
    data = dict(cm = cm, cp=cp)
    return render(request, 'myapp/category_details.html', data)

@method_decorator(login_required, name='dispatch')
class CollectCoupon(View):
  def get(self, request, pk):
    user = UserProfile.objects.get(user=request.user)
    if user.credits > 0:
      cp = Coupon.objects.filter(id=pk)
      cp.update(collected_by=request.user)
      profiledetail = UserProfile.objects.filter(user_id=request.user.id)
      profiledetail.update(credits=F('credits') - 1)
      data = dict(cp=cp, profiledetail=profiledetail)
      return render(request, 'myapp/profile.html', data)
    else:
      messages.warning(request, "Your credits score is Zero, add some coupons to get score")
      return redirect("add-coupon")
    
@method_decorator(login_required, name='dispatch')
class FullDetail(DetailView):
  def get(self, request, pk):
    cp = Coupon.objects.filter(id=pk)
    profiledetail = UserProfile.objects.filter(user_id=request.user.id)
    data = dict(cps=cp, profiledetail=profiledetail)
    return render(request, 'myapp/full_detail.html', data)

@method_decorator(login_required, name='dispatch')
class UpdateProfile(View):
  def get(self, request):
    fm = UserProfileForm(instance=request.user)
    fm2 = UserProfileForm2(instance=request.user.userprofile)
    profiledetail = UserProfile.objects.filter(user_id=request.user.id)
    data = dict(forms=fm, forms2=fm2, profiledetail=profiledetail)
    pprint(data)
    return render(request, 'myapp/profile_update.html', data)
  
  def post(self, request):
    old_image = ""
    if request.user.userprofile.dp:
      old_image = request.user.userprofile.dp.path
    fm = UserProfileForm(data=request.POST, instance=request.user)
    fm2 = UserProfileForm2(request.POST, request.FILES, instance=request.user.userprofile)
    if fm.is_valid() and fm2.is_valid():
      if os.path.exists(old_image):
        print("os.path:",os.path)
        os.remove(old_image)
      fm.save()
      fm2.save()
      messages.success(request, "Profile Updated Successfully")
    else:
      fm = UserProfileForm(request.POST, instance=request.user)
      fm2 = UserProfileForm2(request.POST, instance=request.user.userprofile)
    fm = UserProfileForm(request.POST, instance=request.user)
    fm2 = UserProfileForm2(request.POST, request.FILES, instance=request.user.userprofile)
    profiledetail = UserProfile.objects.filter(user_id=request.user.id)
    data = dict(forms=fm, form2=fm2, profiledetail=profiledetail)
    return render(request, 'myapp/profile_update.html', data)

@method_decorator(login_required, name='dispatch')
class ExpiredCoupons(View):
  def get(self, request):
    profiledetail = UserProfile.objects.filter(user_id=request.user.id)
    cp = Coupon.objects.filter(collected_by=request.user, validity__lt=date.today())
    data = dict(cp=cp, profiledetail=profiledetail)
    return render(request, 'myapp/expired_coupons.html', data)

@method_decorator(login_required, name='dispatch')
class AddedCoupons(View):
  def get(self, request):
    profiledetail = UserProfile.objects.filter(user_id=request.user.id)
    cp = Coupon.objects.filter(added_by=request.user)
    data = dict(cp=cp, profiledetail=profiledetail)
    return render(request, 'myapp/added_coupons.html', data)


class CompanyWise(View):
  def get(self, request, pk):
    if pk:
      cm = Company.objects.filter(id=pk)
      cp = Coupon.objects.filter(company=pk, collected_by=None, validity__gt=date.today())
    else:
      cm = Company.objects.all()
      cp = Coupon.objects.filter(collected_by=None, validity__gt=date.today())
    data = dict(cm = cm, cp=cp)
    return render(request, 'myapp/company_wise.html', data)


# def shop(request):
#   return render(request, 'myapp/shop.html')

class Contact(View):
  def get(self, request):
    return render(request, 'myapp/contact.html')


class Detail(DetailView):
  model = Coupon
  template_name = 'myapp/detail.html'
  context_object_name = 'cp'

class Search(View):
  def post(self, request):
    s = request.POST.get('search').strip()
    print(s)
    search = Coupon.objects.filter((Q(title__icontains=s) | Q(description__icontains=s)), collected_by=None, validity__gt=date.today())
    print(search.query)
    context = dict(search=search, s=s)
    return render(request, 'myapp/search.html', context)
  

  