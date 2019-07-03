from __future__ import unicode_literals

from django.db import models

from django.template.defaultfilters import slugify
from datetime import datetime
from decimal import Decimal
import uuid 


# System Users  
class System_users(models.Model): 
	uuid = models.UUIDField(default=uuid.uuid4)
	ad_name = models.CharField(max_length=128, unique=True) 
	ad_email = models.CharField(max_length=128, unique=True) 
	ad_password = models.CharField(max_length=256) 
	ad_slug = models.SlugField(unique=True, blank=True)
	ad_phone = models.CharField(max_length=30, blank=True)
	state = models.CharField(max_length=128, unique=False, blank=True)
	lga = models.CharField(max_length=128, unique=False, blank=True)
	ad_status = models.CharField(max_length=15, blank=True)
	ad_role = models.CharField(max_length=15, blank=True)
	ad_reg_at = models.DateTimeField(auto_now_add=True)
	ad_reg_by = models.IntegerField(blank=True)

	def save(self, *args, **kwargs): 
		self.ad_slug = slugify(self.ad_name) 
		super(System_users, self).save(*args, **kwargs)


	def __str__(self): #For Python 3, use __unicode__ on Python 2

		return self.ad_name


# Departments
class Department(models.Model): 
	name = models.TextField(max_length=256) 
	description = models.CharField(max_length=128, blank=True)
	slug = models.SlugField(blank=True, max_length=300)
	registered_at = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs): 
		self.slug = slugify(self.name) 
		super(Department, self).save(*args, **kwargs)

	def __str__(self): #For Python 3, use __unicode__ on Python 2

		return self.name


# Staff
class Staff(models.Model): 
	# id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	email = models.CharField(max_length=128)
	fullname = models.CharField(max_length=128, blank=True)  
	phone = models.CharField(max_length=128, unique=False)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
	address = models.CharField(max_length=128, blank=True)
	registered_at = models.DateTimeField(auto_now_add=True)

	def __str__(self): #For Python 3, use __unicode__ on Python 2

		return self.fullname


# Measurable Params
class Measurable_param(models.Model): 
	question_title = models.TextField(max_length=300)
	question_slug = models.SlugField( max_length=400, blank=True)
	question_dept = models.ForeignKey('Department', on_delete=models.CASCADE)
	question_reg_at = models.DateTimeField(auto_now_add=True)
	question_weight = models.CharField(max_length=20, blank=True)
	def save(self, *args, **kwargs): 
		self.question_slug = slugify(self.question_title) 
		super(Measurable_param, self).save(*args, **kwargs)

	def __str__(self): #For Python 3, use __unicode__ on Python 2

		return self.question_title


# Options
class Option(models.Model): 
	option_title = models.TextField(max_length=300) 
	option_question = models.ForeignKey('Measurable_param', related_name='options', on_delete=models.CASCADE) 
	option_weight = models.CharField(max_length=20, blank=True)
	option_value = models.IntegerField(null=True, blank=True, default=0)

	def __str__(self): #For Python 3, use __unicode__ on Python 2

		return self.option_title


# form Data
class Form_data(models.Model): 
	staff = models.ForeignKey('Staff', on_delete=models.CASCADE) 
	question = models.ForeignKey('Measurable_param', on_delete=models.CASCADE)
	answer_value = models.TextField(max_length=256, blank=True) 
	answer = models.ForeignKey('Option', on_delete=models.CASCADE)
	score = models.CharField(max_length=128, blank=True)
	week = models.CharField(max_length=128, blank=True)
	form_registered_at = models.DateTimeField(auto_now_add=True)

	def __str__(self): #For Python 3, use __unicode__ on Python 2

		return str(self.score)


