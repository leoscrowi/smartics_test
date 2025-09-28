import django_filters

from src.domain.core.expense.models import ExpenseEntity
from src.domain.core.category.models import CategoryEntity

class ExpenseFilter(django_filters.FilterSet):
    spent_at_from = django_filters.DateTimeFilter(field_name='spent_at', lookup_expr='gte', label='Spent from')
    spent_at_to = django_filters.DateTimeFilter(field_name='spent_at', lookup_expr='lte', label='Spend before')

    value_min = django_filters.NumberFilter(field_name='value', lookup_expr='gte', label='Minimum value')
    value_max = django_filters.NumberFilter(field_name='value', lookup_expr='lte', label='Maximum value')

    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='categories',
        to_field_name='id',
        queryset=None,
        label='categories'
    )

    class Meta:
        model = ExpenseEntity
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['categories'].queryset = CategoryEntity.objects.all()