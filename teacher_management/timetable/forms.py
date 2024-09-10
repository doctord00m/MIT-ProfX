from django import forms
from .models import TimetableChangeRequest

class TimetableChangeRequestForm(forms.ModelForm):
    class Meta:
        model = TimetableChangeRequest
        fields = ['original_class', 'proposed_day', 'proposed_start_time', 'proposed_end_time']