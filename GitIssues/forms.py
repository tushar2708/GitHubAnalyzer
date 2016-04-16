from django import forms

from GitIssues.models import Query
from GitIssues.models import Result


class QueryForm(forms.ModelForm):

    class Meta:
        model = Query
        fields = ('GitHubPublicRepo',)
