from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=100)
  image = models.ImageField(upload_to='category_images')

  def __str__(self):
    return self.name

class Company(models.Model):
  name = models.CharField(max_length=100)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class Coupon(models.Model):
  title = models.CharField(max_length=500)
  description = models.TextField()
  code = models.CharField(max_length=100)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='add', default="")
  collected_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collect", null=True, blank=True)
  validity = models.DateField()
  used = models.BooleanField(default=False)
  image = models.ImageField(upload_to='coupon_image/', null=True)

  # def delete(self, using=None, keep_parents=False):
  #   self.image.storage.delete(self..name)
  #   self.image.storage.delete(self.song.name)
  #   super().delete()


  

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  credits = models.IntegerField(default=5)
  dp = models.ImageField(upload_to='user_dp/', null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()

