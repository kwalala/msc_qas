from django import forms
from course.models import Course
from django.forms.extras.widgets import SelectDateWidget
  
from uni_form.helpers import FormHelper, Submit

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ("admin", "date_created", "developers", "activated", "complete",)
    #date_target = forms.DateField(widget=SelectDateWidget())
    helper = FormHelper()
    #helper.add_input(Submit('_cancel', _('Cancel')))
    helper.add_input(Submit('submit', 'Next'))