from django import forms


class ForeignExchangeForm(forms.Form):
    curr1 = forms.CharField(label="Currency 1", max_length=10)
    curr2 = forms.CharField(label="Currency 2", max_length=10)


class SearchStockByName(forms.Form):
    stock_name = forms.CharField(label="Stock Name", max_length=20)
