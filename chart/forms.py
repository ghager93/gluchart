from django import forms


class AddSourceForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50)
    type = forms.ChoiceField(choices={
        "libre_link_up": "Libre Link Up"
    })
    api_key = forms.CharField(label="API Key", max_length=200)