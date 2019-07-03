from rest_framework import serializers

from api.models import System_users, Department, Staff, Measurable_param, Option, Form_data

# System Users 
class System_usersSerializer(serializers.ModelSerializer):
	class Meta:
		model = System_users
		fields = ('id', 'ad_name', 'ad_email', 'ad_slug', 'ad_role', 'ad_password', 'ad_phone', 'ad_status', 'ad_reg_at', 'ad_reg_by')


					
# Department 
class DepartmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Department
		fields = ('id', 'name', 'description', 'slug', 'registered_at')
	
					
			
# Staff 
class StaffSerializer(serializers.ModelSerializer):
	class Meta:
		model = Staff
		fields = ('id', 'fullname', 'department', 'phone', 'address', 'email', 'registered_at')
			
class StaffNestedSerializer(serializers.ModelSerializer):
	department = DepartmentSerializer()
	class Meta:
		model = Staff
		fields = ('id', 'fullname', 'department', 'phone', 'address', 'email', 'registered_at')
			
			
# Option 
class OptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Option
		fields = ('id','option_title', 'option_question', 'option_weight', 'option_value')
		

					
# Measurable_param 
class Measurable_paramSerializer(serializers.ModelSerializer):
	class Meta:
		model = Measurable_param
		fields = ('id','question_title','question_slug','question_dept','question_reg_at', 'question_weight')
	
					
class Measurable_paramNestedSerializer(serializers.ModelSerializer):
	question_dept = DepartmentSerializer()
	options = OptionSerializer(many=True)
	class Meta:
		model = Measurable_param
		fields = ('id','question_title','question_slug','question_dept','question_reg_at', 'options', 'question_weight')


					
# Form_data 
class Form_dataSerializer(serializers.ModelSerializer):
	class Meta:
		model = Form_data
		fields = ('id', 'staff', 'question', 'answer_value', 'answer', 'score', 'form_registered_at', 'week')

				


class Form_dataNestedSerializer(serializers.ModelSerializer):
	question = Measurable_paramSerializer()
	staff = StaffSerializer()
	answer = OptionSerializer()
	class Meta:
		model = Form_data
		fields = ('id', 'staff', 'question', 'answer_value', 'answer', 'score', 'form_registered_at', 'week')

				

