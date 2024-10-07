from django_filters import rest_framework as filters
from .models import Platos

class PlatosFilter(filters.FilterSet):
    nombre_plato = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Platos
        fields = ['nombre_plato']