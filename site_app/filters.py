import django_filters
from site_app import models

class MasterFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=models.Category.objects.all())
    class Meta:
        model = models.Master
        fields = ['category']


class ServiceFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=models.Category.objects.all())

    class Meta:
        model = models.Service
        fields = ['category']


class MasterSearchFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.Master
        fields = ['name']