from django import forms
from .models import RFQ
from datetime import datetime

class RFQForm(forms.ModelForm):
    class Meta:
        model = RFQ
        fields = ['item', 'due_date', 'amount_required_lbs', 'ship_to_location', 'required_certifications']
        widgets = {
            'due_date': forms.DateInput(attrs={
                'type': 'date', 
                'min': datetime.now().strftime('%Y-%m-%d'),
                'input_format': '%Y-%m-%d'
            }),
            'amount_required_lbs': forms.NumberInput(attrs={'step': '1'}),
            'ship_to_location': forms.Textarea(attrs={'rows': 1}),
            'required_certifications': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_item(self):
        item = self.cleaned_data.get('item')
        if not isinstance(item, str):
            raise forms.ValidationError("Item must be a string.")
        return item

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if not due_date:
            raise forms.ValidationError("Due date must be a valid date.")
        return due_date

    def clean_ship_to_location(self):
        ship_to_location = self.cleaned_data.get('ship_to_location')
        if not isinstance(ship_to_location, str):
            raise forms.ValidationError("Ship to location must be a string.")
        return ship_to_location

    def clean_required_certifications(self):
        required_certifications = self.cleaned_data.get('required_certifications')
        if not isinstance(required_certifications, str):
            raise forms.ValidationError("Required certifications must be a comma-separated string.")
        return required_certifications