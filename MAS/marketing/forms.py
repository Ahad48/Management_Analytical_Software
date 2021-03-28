from django import forms


class SearchCompanyForm(forms.Form):
    company_name = forms.CharField(label="Company", max_length=100)
