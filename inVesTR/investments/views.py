import base64
from io import BytesIO

from django.db.models import F, OuterRef, Subquery
from django.shortcuts import get_object_or_404, redirect, render
from matplotlib import pyplot as plt

from .forms import InvestmentForm
from .models import Investment


def index(request):
    latest_updates = Investment.objects.filter(
        investment_code=OuterRef('investment_code'),
        institution=OuterRef('institution')
    ).order_by('-updated_at')

    investments = Investment.objects.annotate(max_updated_at=F('updated_at'))\
        .filter(
        updated_at=Subquery(latest_updates.values('updated_at')[:1])
    )

    for investment in investments:
        penultimate_update = Investment.objects.filter(
            investment_code=investment.investment_code,
            institution=investment.institution,
            updated_at__lt=investment.updated_at
        ).order_by('-updated_at').first()

        if penultimate_update:
            last_profit = (
                (investment.current_value - penultimate_update.current_value) /
                penultimate_update.current_value) * 100
            investment.last_profit = round(last_profit, 2
                                           )
        else:
            investment.last_profit = None

        oldest_update = Investment.objects.filter(
            investment_code=investment.investment_code,
            institution=investment.institution
        ).order_by('updated_at').first()

        if oldest_update:
            total_profit = ((investment.current_value -
                            oldest_update.current_value) /
                            oldest_update.current_value) * 100
            investment.total_profit = round(total_profit, 2)
        else:
            investment.total_profit = None

    context = {'investments': investments}

    # Check if there are no investments
    if not investments:
        context['no_investments'] = True

    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = InvestmentForm()

    context['form'] = form
    context['no_investments'] = not investments.exists()

    return render(request, 'index.html', context)


def update_investment(request, pk):
    investment = get_object_or_404(Investment, pk=pk)

    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        form.is_valid()
        if form.cleaned_data['current_value'] is not None:
            new_investment = Investment(
                investment_code=investment.investment_code,
                institution=investment.institution,
                current_value=form.cleaned_data['current_value'],
            )
            print(new_investment)
            new_investment.save()
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = InvestmentForm()

    context = {'form': form, 'investment': investment}
    return render(request, 'update_investment.html', context=context)


def delete_investment(request, pk):
    investment = Investment.objects.get(pk=pk)
    investment.delete()
    return redirect('index')


def investment_chart(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    updates = Investment.objects.filter(
        investment_code=investment.investment_code,
        institution=investment.institution
    ).order_by('updated_at')

    dates = [update.updated_at for update in updates]
    values = [update.current_value for update in updates]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Current Value')
    plt.title(
        f'Investment Chart - {investment.investment_code}\
            ({investment.institution})')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return render(request, 'investment_chart.html', {'chart_data': chart_data})
