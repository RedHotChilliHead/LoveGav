from django import forms
from django.forms import ModelForm
from .models import Answer


class Calculator(forms.Form):
    weight = forms.FloatField(label='Weight (kg)')
    calorie_content = forms.FloatField(label='Сalorie content (kcal/kg)', required=False)
    k1 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
                            label='Light physical activity', required=False)  # 1.2
    k2 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-class'}), label='Hard work',
                            required=False)  # 3
    k3 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
                            label='Without physical activity', required=False)  # 0.8
    k4 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
                            label='Feeds the puppies', required=False)  # 2.4
    k5 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
                            label='Just born (0-3 months)', required=False)  # 2
    k6 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
                            label='Large breed puppy (3-9 months old)', required=False)  # 1.6
    k7 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
                            label='Large breed puppy (9-24 months old)', required=False)  # 1.2
    k8 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
                            label='Puppy of medium and small breeds (3-6 months)', required=False)  # 1.6
    k9 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
                            label='Puppy of medium and small breeds (3-6 months)', required=False)  # 1.6
    k10 = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
                             label='Puppy of medium and small breeds (6-12 months)', required=False)  # 1.2


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ["body", "photo"]
