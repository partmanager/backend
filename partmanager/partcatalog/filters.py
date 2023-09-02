import django_filters
from .models.capacitor import Capacitor


class CapacitorFilter(django_filters.FilterSet):
    capacitance_in_femtofarads = django_filters.RangeFilter()
    voltage = django_filters.RangeFilter()
    #tolerance_value = django_filters.RangeFilter()

    production_status = django_filters.MultipleChoiceFilter(choices=Capacitor.PRODUCTION_STATUS)
#    capacitor_type = django_filters.MultipleChoiceFilter(choices=Capacitor.CAPACITOR_TYPE)
    dielectric_type = django_filters.MultipleChoiceFilter(choices=Capacitor.DielectricType.choices)

    class Meta:
        model = Capacitor
        fields = ['production_status', #'capacitance_in_farads_typ', 'tolerance_value', 'voltage', 'capacitor_type',
                  'dielectric_type', 'manufacturer']

