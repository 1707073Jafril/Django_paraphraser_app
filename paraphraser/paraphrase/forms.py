# paraphrase/forms.py

from django import forms

class ParaphraseForm(forms.Form):
    paragraph = forms.CharField(widget=forms.Textarea, label='Input Paragraph')
