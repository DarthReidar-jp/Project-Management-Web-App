from django import forms

class FormClass(forms.Form):
    title = forms.CharField()
    content = forms.CharField()
