from django import forms

class Calculator(forms.Form):
    weight = forms.FloatField(label='Weight')