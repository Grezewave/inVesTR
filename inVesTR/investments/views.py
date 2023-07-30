from django.shortcuts import render
from flask import redirect

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
    context['no_investments'] = not bool

    return render(request, 'index.html', context)
