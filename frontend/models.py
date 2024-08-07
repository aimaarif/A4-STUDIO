from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


# Categories of Products
class Category(models.Model):
	name = models.CharField(max_length=50)
	image = models.ImageField(upload_to='uploads/category/', default="none")


	def __str__(self):
		return self.name

	#@daverobb2011
	class Meta:
		verbose_name_plural = 'categories'

class Product(models.Model):
	name = models.CharField(max_length=200)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	image = models.ImageField(upload_to='uploads/product/')


	def __str__(self):
		return self.name