from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    # path('category-details/', views.shop, name="category-detail"),
    path('detail/<int:pk>/', views.Detail.as_view(), name='detail'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('add-coupon/', views.AddCoupon.as_view(), name="add-coupon"),
    path('category/<int:pk>/', views.CategoryShow.as_view(), name="category"),
    path('collect/<int:pk>/', views.CollectCoupon.as_view(), name="collect"),
    path('add-company/', views.AddCompany.as_view(), name="add-company"),
    path('add-category/', views.AddCategory.as_view(), name="add-category"),
    path('full-detail/<int:pk>', views.FullDetail.as_view(), name="full-detail"),
    path('added-coupons/', views.AddedCoupons.as_view(), name="added-coupons"),
    path('expired-coupons/', views.ExpiredCoupons.as_view(), name="expired-coupons"),
    path('company-wise/<int:pk>', views.CompanyWise.as_view(), name="company-wise"),

    path('profile-update/', views.UpdateProfile.as_view(), name="profile-update"),
    path('contact/', views.Contact.as_view(), name="contact"),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='myapp/login.html', authentication_form=LoginForm), name='login'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name="myapp/passwordchange.html", form_class=MyPasswordChangeForm, success_url="/passwordchangedone/"), name="changepassword"),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name="myapp/passwordchangedone.html"), name="passswordchangedone"),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="myapp/password_reset.html", form_class=MyPasswordResetForm), name="password-reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_reset_complete.html'), name="password_reset_complete"),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path('registration/', views.CustomerRegistration.as_view(), name='customerregistration'),

    path('search/', views.Search.as_view(), name="search"),

]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



