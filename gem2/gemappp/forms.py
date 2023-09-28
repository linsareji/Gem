from django.utils.datetime_safe import date

from .models import *
from django import forms


class AdmissionForm(forms.ModelForm):
    class Meta:
        model=StudentAdmission
        fields=['gemid','stud_name','parent_name','parent_contact','stud_address','stud_contact',
                'qualification','dob','gender','course1','course2','course_duration','scheme',
                'fee','joining_date','exam_date','certificate_status','student_status']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AdmissionFormPage(forms.ModelForm):
    stud_contact = forms.IntegerField()
    class Meta:
        model=Admission
        fields=['regno','stud_name','parent_name','parent_contact','stud_address','stud_contact',
                'qualification','dob','gender','course','course_duration','scheme',
                'fee','joining_date','exam_date','certificate_status','student_status']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['joining_date'].initial = date.today()
        self.fields['gender'].empty_label = "Select Gender"
        self.fields['course'].empty_label = "Select Course"
        self.fields['scheme'].empty_label = "Select Scheme"
        self.fields['fee'].widget.attrs['placeholder'] = "Enter Fee"
        self.fields['course_duration'].widget.attrs['placeholder'] = "Enter Course duration"


class DropdownForm(forms.Form):
    college = forms.ModelChoiceField(queryset=Add_collage.objects.all(),empty_label="Select College",widget=forms.Select(attrs={'class': 'dropdown'}))
    staff = forms.ModelChoiceField(queryset=Add_staff.objects.all(),empty_label="Select Staff",widget=forms.Select(attrs={'class': 'dropdown'}))
    course = forms.ModelChoiceField(queryset=Add_course.objects.all(),empty_label="Select course",widget=forms.Select(attrs={'class': 'dropdown'}))
    scheme = forms.ModelChoiceField(queryset=Add_scheme.objects.all(),empty_label="Select Scheme",widget=forms.Select(attrs={'class': 'input-text'}))


class TieupPageForm(forms.ModelForm):
    class Meta:
        model = Tieup
        fields = ['college', 'course', 'fee','course_duration','tieup_date']
        widgets = {
            'tieup_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial value for tieup_date to today's date
        self.fields['tieup_date'].initial = date.today()
        # Add empty_label and widget attributes to the college field
        self.fields['college'].empty_label = "Select College"
        # self.fields['college'].widget = forms.Select(attrs={'class': 'dropdown'})
        self.fields['course'].empty_label = "Select Course"
        self.fields['fee'].widget.attrs['placeholder'] = "Enter Fee"
        self.fields['course_duration'].widget.attrs['placeholder'] = "Enter Course duration"
        # self.fields['course'].widget = forms.Select(attrs={'class': 'dropdown'})
class SessionPageForm(forms.ModelForm):
    class Meta:
        model=Session
        fields=['college','course','staff','duration','date','remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today()
        # Add empty_label and widget attributes to the college field
        self.fields['college'].empty_label = "Select College"
        self.fields['course'].empty_label = "Select Course"
        self.fields['staff'].empty_label = "Select Staff"
        self.fields['duration'].widget.attrs['placeholder'] = "Enter Course duration"
        self.fields['remarks'].widget.attrs['placeholder'] = "Enter  remarks"


class DiscontinueForm(forms.ModelForm):
    class Meta:
        model = Discontinue
        fields = ['regno', 'name', 'course', 'discontinue_date', 'remarks']
        widgets = {
            'discontinue_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EnquiryForm(forms.ModelForm):
    class Meta:
        model=StudentEnquiry
        fields=['name','address','contact','course','enq_date']
        widgets = {
            'enq_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enq_date'].initial = date.today()
        # Add empty_label and widget attributes to the college field
        self.fields['name'].widget.attrs['placeholder'] = "Enter Student name"
        self.fields['address'].widget.attrs['placeholder'] = "Enter address"
        self.fields['contact'].widget.attrs['placeholder'] = "Enter  contact number"
        self.fields['course'].widget.attrs['placeholder'] = "Enter Course"
