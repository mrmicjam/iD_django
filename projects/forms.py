from django import forms
import urllib
import json


class CreateForm(forms.Form):
    project_name = forms.CharField(max_length=200)
    location = forms.CharField(max_length=500, help_text="Street address or zip code")

    def clean_location(self):
        location = self.cleaned_data["location"]
        params = {
            "address": location,
            "sensor": "false"
        }
        params = urllib.urlencode(params)
        f = urllib.urlopen("https://maps.googleapis.com/maps/api/geocode/json?%s" % params)
        results = json.loads(f.read())
        if not "results" in results:
            raise forms.ValidationError("Unable to find location")
        first_result = results["results"][0]

        location = first_result["geometry"]["location"]
        return location  # dict with lat/lng
