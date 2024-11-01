import django_filters
from site_app import models

class MasterFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=models.Category.objects.all())
    class Meta:
        model = models.Master
        fields = ['category']