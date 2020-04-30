import django_filters
from .models import *

class ProjectFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model= Project
        fields= ['category'] #, 'title']

