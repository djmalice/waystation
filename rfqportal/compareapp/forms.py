from django import forms
from .models import RFQ

class RFQForm(forms.ModelForm):
    class Meta:
        model = RFQ
        fields = ['item', 'due_date', 'amount_required_lbs', 'ship_to_location', 'required_certifications']