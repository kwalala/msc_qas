from django import forms
from course.models import Course, Milestone
from django.forms.extras.widgets import SelectDateWidget
  
from uni_form.helpers import FormHelper, Submit

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ("admin", "date_created", "developers", "activated", "complete",)
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Next'))
    
    
class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ("name", "approver", "date_target")
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Save Changes'))