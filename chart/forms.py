from django import forms

from .models import Source


class SourceForm(forms.ModelForm):
    type = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["type"].choices = [
            ("libre_link_up", "Libre Link Up")
        ]
    class Meta:
        model = Source
        fields = ["name", "type", "api_key"]


class LibreLinkUp(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50, label="LibreLinkUp Email")
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(), label="LibreLinkUp Password")
