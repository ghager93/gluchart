from django import forms

from .models import Source


class AddSourceForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50)
    type = forms.ChoiceField(choices={
        "libre_link_up": "Libre Link Up"
    })
    api_key = forms.CharField(label="API Key", max_length=200)


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
