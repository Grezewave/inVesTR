from django.shortcuts import get_object_or_404, redirect, render

from .forms import InvestmentForm
from .models import Investment


def index(request):
    investments = Investment.objects.all()
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
