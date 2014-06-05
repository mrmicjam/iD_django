from django import forms
import urllib
import json
import re
from django.utils.translation import ugettext as _
from django.core.validators import validate_email


SEPARATOR_RE = re.compile(r'[,;]+')

def validate_email_list(value):
    emails = SEPARATOR_RE.split(value)
    for email in emails:
        validate_email(email)


class EmailsListField(forms.CharField):

    widget = forms.Textarea

    def clean(self, value):
        super(EmailsListField, self).clean(value)

        emails = re.compile(r'[^\w\.\-\+@_]+').split(value)

        if not emails:
            raise forms.ValidationError(_(u'Enter at least one e-mail address.'))

        for email in emails:
            validate_email(email)

        return emails


class InvitationForm(forms.Form):
    emails = EmailsListField()


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

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=500, required=True)

