from django.shortcuts import render
from .forms import TestModelForm
from .models import TestModel
from .seralizeres import TestModelSerializer
from rest_framework import generics, viewsets


def show_page(request):
    success = False
    if request.method == 'POST':
        form = TestModelForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            TestModel.objects.create(text=cd['text'], title=cd['title'])
            success = True
            form = TestModelForm()
    else:
        form = TestModelForm()

    name = 'jack'
    return render(request, 'home_page.html', {'name': name, 'form': form, 'success': success})


class TestModelList(viewsets.ReadOnlyModelViewSet):
    """Api end point"""
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer

    def get_queryset(self):
        queryset = TestModel.objects.all()

        if self.request.query_params.get('titles[]'):
            queryset = queryset.filter(title__in=self.request.query_params.getlist('titles[]'))

        return queryset

