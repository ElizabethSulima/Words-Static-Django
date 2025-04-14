from django import forms


class UploadForm(forms.Form):
    my_file = forms.FileInput()
