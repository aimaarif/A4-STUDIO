from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional fields you want here, e.g., profile picture, bio, etc.
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='uploads/profile_pics/', default='uploads/profile_pics/default.png', blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    

    def __str__(self):
        return f"{self.user.first_name} ({self.user.username})"
    
    def follow(self, profile):
        """Follow another user's profile."""
        self.following.add(profile)
        
    def unfollow(self, profile):
        """Unfollow another user's profile."""
        self.following.remove(profile)
   


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"


class MainCategory(models.Model):
	name = models.CharField(max_length=50)
	image = models.ImageField(upload_to='uploads/maincategory/', default="none")

	def __str__(self):
		return self.name

	#@daverobb2011
	class Meta:
		verbose_name_plural = 'maincategories'


class Category(models.Model):
	name = models.CharField(max_length=50)
	image = models.ImageField(upload_to='uploads/category/', default="none")
	maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, default=1)


	def __str__(self):
		return self.name

	#@daverobb2011
	class Meta:
		verbose_name_plural = 'categories'

class Product(models.Model):
	name = models.CharField(max_length=200)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	image = models.ImageField(upload_to='uploads/product/')
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


	def __str__(self):
		return self.name
      
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)  # Rating out of 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating} Stars"