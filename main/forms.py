from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
    force = forms.BooleanField(initial=False, required=False)
