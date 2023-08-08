from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:pk>/', views.delete_investment,
         name='delete_investment'),  # URL para a view de deleção
    path('update/<int:pk>/', views.update_investment,
         name='update_investment'),
    path('investment/<int:pk>/chart/',
         views.investment_chart, name='investment_chart'),
]
