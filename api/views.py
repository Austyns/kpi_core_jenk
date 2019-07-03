from django.shortcuts import render
# from django.db import connections
# from django.db import connection
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet


from rest_framework import filters
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
# import requests
import json

from api.models import System_users, Department, Staff, Measurable_param, Option, Form_data

from api.serializers import System_usersSerializer, DepartmentSerializer, StaffSerializer, StaffNestedSerializer, Measurable_paramSerializer, Measurable_paramNestedSerializer, OptionSerializer, Form_dataSerializer, Form_dataNestedSerializer


import hashlib, uuid

SALT_STR = "3442edfdgdh273yy3nBHD4jfhbdn-DJndjdn9jf3938jndcucjm-mdjdnueen-D4Hflsd#udy@ndnd_MDMDiedm3984hn0jkjn"


# Create your views here.

#System Administrators  
class systemAdmins(generics.ListCreateAPIView):
	queryset = System_users.objects.all()
	serializer_class = System_usersSerializer

	def post(self, request, *args, **kwargs):
		hashed = hashlib.sha512( (request.data['ad_password'] + SALT_STR).encode("utf-8") ).hexdigest()
		request.data['ad_password'] = hashed
		return self.create(request, *args, **kwargs)


class systemAdminDetails(generics.RetrieveUpdateAPIView):
	queryset = System_users.objects.all()
	serializer_class = System_usersSerializer

# System User Login
class loginUser(generics.CreateAPIView):
	serializer_class = System_usersSerializer

	# def get(self, *args, **kwargs):
	# 	return JsonResponse({"message": "Method Not supported"})

	def post(self, request, *args, **kwargs):
		email = request.data.get('ad_email')
		password = request.data.get('ad_pass')
		# hashed = hashlib.sha512(( str(password) + str( SALT_STR)).encode("utf-8") ).hexdigest()
		hashed = password
		user = System_users.objects.filter(ad_email=email, ad_password=hashed).values()

		if user:
			del (user[0]['ad_password'])
			# print(user)
			return JsonResponse({"data": list(user), "status": "success"})
		else:
			return JsonResponse({"data": [], "status": "fail", "message": "Invalid login cridentials"})



# Department  
class departments(generics.ListCreateAPIView):
	queryset = Department.objects.all()
	serializer_class = DepartmentSerializer

class departmentDetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = Department.objects.all()
	serializer_class = DepartmentSerializer


# Staff   
class staffs(generics.CreateAPIView):
	"""This method creates a new staff [See parameters from example below] """
	queryset = Staff.objects.all()
	serializer_class = StaffSerializer

class staffGet(generics.ListAPIView):
	queryset = Staff.objects.all()
	serializer_class = StaffNestedSerializer

class staffDetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = Staff.objects.all()
	serializer_class = StaffNestedSerializer



# Option  
class options(generics.ListCreateAPIView):
	queryset = Option.objects.all()
	serializer_class = OptionSerializer

	def get_serializer(self, *args, **kwargs):
	    if "data" in kwargs:
	        data = kwargs["data"]
	        # check if many is required
	        if isinstance(data, list):
	            kwargs["many"] = True
	    return super(options, self).get_serializer(*args, **kwargs)


class optionDetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = Option.objects.all()
	serializer_class = OptionSerializer


# Measurable_param  
class questions(generics.CreateAPIView):
	queryset = Measurable_param.objects.all()
	serializer_class = Measurable_paramSerializer

class questionDetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = Measurable_param.objects.all()
	serializer_class = Measurable_paramSerializer


class getQuestions(generics.ListAPIView):
	queryset = Measurable_param.objects.all()
	serializer_class = Measurable_paramNestedSerializer


class questionsByCategory(generics.ListAPIView):
	# queryset = City.objects.all()
	serializer_class = Measurable_paramNestedSerializer

	def get_queryset(self):
		Cid = self.kwargs['cId']
		_questions = Measurable_param.objects.filter(question_dept=Cid)
		return _questions


# Form_data  
class formDatas(generics.ListCreateAPIView):
	queryset = Form_data.objects.all()
	serializer_class = Form_dataSerializer

	def get_serializer(self, *args, **kwargs):
	    if "data" in kwargs:
	        data = kwargs["data"]

	        # check if many is required
	        if isinstance(data, list):
	            kwargs["many"] = True

	    return super(formDatas, self).get_serializer(*args, **kwargs)

class getformData(generics.ListAPIView):
	queryset = Form_data.objects.all()
	serializer_class = Form_dataNestedSerializer

class formDataDetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = Form_data.objects.all()
	serializer_class = Form_dataSerializer

class formDataDetail(generics.ListAPIView):
	# queryset = Form_data.objects.all()
	serializer_class = Form_dataNestedSerializer

	def get_queryset(self):
		submissionId = self.kwargs['submissionId']
		_response = Form_data.objects.filter(submission_ref=submissionId)
		return _response

class formDataByUser(generics.ListAPIView):
	# queryset = Form_data.objects.all()
	serializer_class = Form_dataNestedSerializer

	def get_queryset(self):
		uId = self.kwargs['uId']
		_response = Form_data.objects.filter(staff=uId)
		return _response


