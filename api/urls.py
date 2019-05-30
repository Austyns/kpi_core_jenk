# from django.conf.urls import url, include

# from django.conf.urls import  url
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
                
        	# System Admins 
        	re_path(r'^systemAdmins/$', views.systemAdmins.as_view()),
                re_path(r'^systemAdmin/(?P<pk>.+)/$', views.systemAdminDetails.as_view()), 
                re_path(r'^login/?$', views.loginUser.as_view()), 

                # departments
                re_path(r'^departments/?$', views.departments.as_view()),
                re_path(r'^department/(?P<pk>[0-9]+)/$', views.departmentDetails.as_view()), 

                # staffs
                re_path(r'^staffs/?$', views.staffs.as_view()),
                re_path(r'^getStaffs/?$', views.staffGet.as_view()),
                re_path(r'^staff/(?P<pk>[0-9]+)/$', views.staffDetails.as_view()), 


                # option
                re_path(r'^options/?$', views.options.as_view()),
                re_path(r'^option/(?P<pk>[0-9]+)/$', views.optionDetails.as_view()), 


                # question
                re_path(r'^questions/$', views.questions.as_view()),
                re_path(r'^getQuestions/$', views.getQuestions.as_view()),
                re_path(r'^question/(?P<pk>[0-9]+)/$', views.questionDetails.as_view()),
                re_path(r'^cat-questions/(?P<cId>.+)/$', views.questionsByCategory.as_view()),

                # form_data
                re_path(r'^form_data/$', views.formDatas.as_view()),
                re_path(r'^getformData/$', views.getformData.as_view()),
                # re_path(r'^form_data/(?P<submissionId>.+)/$', views.formDataDetail.as_view()), 
                re_path(r'^usersRecords/(?P<uId>.+)/$', views.formDataByUser.as_view()), 
]
urlpatterns = format_suffix_patterns(urlpatterns)