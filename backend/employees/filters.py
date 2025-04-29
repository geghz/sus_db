import django_filters
from datetime import date, timedelta
from django.db.models import Q, Min, OuterRef, Subquery, F
from .models import Employee
from fields.models import FieldDefinition, FieldGroup, EmployeeFieldValue
from rest_framework.filters import OrderingFilter


class EmployeeFilter(django_filters.FilterSet):
    direction = django_filters.NumberFilter(field_name='direction__id')
    manager   = django_filters.NumberFilter(field_name='manager__id')
    tags      = django_filters.ModelMultipleChoiceFilter(
                    field_name='tags__id',
                    to_field_name='id',
                    queryset=Employee._meta.get_field('tags').related_model.objects.all()
                )
    expiry_in = django_filters.NumberFilter(method='filter_expiry_in')

    class Meta:
        model  = Employee
        fields = ['direction', 'manager', 'tags']

    def filter_expiry_in(self, queryset, name, days):
        """
        Отбирает сотрудников, у которых в любых 
        датированных полях (FieldDefinition.has_expiry=True)
        срок истечения в ближайшие `days` дней.
        """
        cutoff = date.today() + timedelta(days=days)
        # Сначала получаем все FieldDefinition, в которых отмечено has_expiry=True
        expiry_defs = FieldDefinition.objects.filter(has_expiry=True)
        # Затем по EmployeeFieldValue ищем те записи, которые относятся к этим определениям
        # и у которых date_value в диапазоне [today, cutoff]
        return queryset.filter(
            employeefieldvalue__field_definition__in=expiry_defs,
            employeefieldvalue__date_value__gte=date.today(),
            employeefieldvalue__date_value__lte=cutoff
        ).distinct()
    
class DynamicFieldOrderingFilter(OrderingFilter):
    """
    Позволяет сортировать по:
     • обычным полям Employee (last_name, direction__name и т.п.)
     • динамическим полям FieldDefinition — параметр запроса ?ordering=field_<code>
     • динамическим группам с датами — ?ordering=group_<code>
    """

    def filter_queryset(self, request, queryset, view):
        ordering_params = self.get_ordering(request, queryset, view)
        if not ordering_params:
            return queryset

        annotations = {}
        order_by = []

        for raw in ordering_params:
            desc = raw.startswith('-')
            name = raw[1:] if desc else raw

            # 1) стандартное поле модели
            if name in {f.name for f in queryset.model._meta.get_fields()}:
                order_by.append(raw)
                continue

            # 2) динамическое одиночное поле: field_<code>
            if name.startswith('field_'):
                code = name[len('field_'):]
                try:
                    fd = FieldDefinition.objects.get(code=code)
                except FieldDefinition.DoesNotExist:
                    continue
                ann_name = f'fd_{fd.id}'
                if ann_name not in annotations:
                    # в зависимости от типа поля выбираем нужный атрибут
                    if fd.field_type == FieldDefinition.TYPE_DATE:
                        sub = EmployeeFieldValue.objects.filter(
                            employee=OuterRef('pk'),
                            field_definition=fd
                        ).values('date_value')[:1]
                    elif fd.field_type == FieldDefinition.TYPE_NUMBER:
                        sub = EmployeeFieldValue.objects.filter(
                            employee=OuterRef('pk'),
                            field_definition=fd
                        ).values('num_value')[:1]
                    else:
                        sub = EmployeeFieldValue.objects.filter(
                            employee=OuterRef('pk'),
                            field_definition=fd
                        ).values('text_value')[:1]
                    annotations[ann_name] = Subquery(sub)
                order_by.append(f'-{ann_name}' if desc else ann_name)
                continue

            # 3) динамическая группа с датами: group_<code>
            if name.startswith('group_'):
                grp_code = name[len('group_'):]
                try:
                    grp = FieldGroup.objects.get(code=grp_code)
                except FieldGroup.DoesNotExist:
                    continue
                # отбираем только date-поля в этой группе
                expiry_defs = grp.fields.filter(field_type=FieldDefinition.TYPE_DATE)
                if not expiry_defs.exists():
                    continue
                ann_name = f'grp_{grp.id}_expiry'
                if ann_name not in annotations:
                    annotations[ann_name] = Min(
                        'employeefieldvalue__date_value',
                        filter=Q(
                            employeefieldvalue__field_definition__in=expiry_defs
                        )
                    )
                order_by.append(f'-{ann_name}' if desc else ann_name)
                continue

            # всё остальное игнорируем
        if annotations:
            queryset = queryset.annotate(**annotations)
        if order_by:
            queryset = queryset.order_by(*order_by)
        return queryset
