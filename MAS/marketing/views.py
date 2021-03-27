from django.shortcuts import render
from .Sentiment import articles
from .forms import SearchCompanyForm


def get_company(request):
    if request.method == 'POST':
        form = SearchCompanyForm(request.POST)
        company_name = request.POST['company_name']
        if form.is_valid():
            df = articles(company_name)
            company_table = df.to_html()
            return render(request, 'marketing/sentiment_result.html', context={'company_table': company_table})
    else:
        form = SearchCompanyForm()
    return render(request, 'marketing/sentiment.html', context={'form': form})

