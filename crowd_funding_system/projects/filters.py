import django_filters
from .models import *

class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model= Project
        fields= ['category', 'title']

