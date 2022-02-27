from typing import List

from api.filters import BaseToolFilter
from django.db.models import QuerySet
from django_filters.rest_framework import filters
from django_filters.rest_framework.filters import OrderingFilter
from findings.enums import OSType
from findings.models import (OSINT, Credential, Endpoint, Enumeration, Exploit,
                             Host, Technology, Vulnerability)

# Common ordering anf filtering fields for all Finding models
FINDING_ORDERING = (
    ('executions__task', 'task'),
    ('executions__task__target', 'target'),
    ('executions__task__target__project', 'project'),
    ('executions__task__tool', 'task__tool'),
    ('executions__step__tool', 'step__tool'),
    ('executions__task__executor', 'executor'),
    'executions',
    'creation',
    'is_active'
)
FINDING_FILTERING = {
    'executions': ['exact'],
    'executions__task': ['exact'],
    'executions__task__target': ['exact'],
    'executions__task__target__target': ['exact', 'icontains'],
    'executions__task__target__project': ['exact'],
    'executions__task__target__project__name': ['exact', 'icontains'],
    'executions__task__executor': ['exact'],
    'executions__task__executor__username': ['exact', 'icontains'],
    'executions__start': ['gte', 'lte', 'exact'],
    'executions__end': ['gte', 'lte', 'exact'],
    'creation': ['gte', 'lte', 'exact'],
    'is_active': ['exact'],
}


class FindingFilter(BaseToolFilter):
    '''Common FilterSet to filter and sort findings entities.'''

    tool_fields: List[str] = ['executions__task__tool', 'executions__step__tool']   # Filter by two Tool fields


class BaseVulnerabilityFilter(FindingFilter):
    '''Common FilterSet to filter findings entities based on vulnerability fields.'''

    enumeration = filters.NumberFilter(method='filter_enumeration')             # Filter by enumeration
    enumeration_port = filters.NumberFilter(method='filter_enumeration_port')   # Filter by enumeration port
    host = filters.NumberFilter(method='filter_host')                           # Filter by host
    host_address = filters.CharFilter(method='filter_host_address')             # Filter by host address
    host_os_type = filters.ChoiceFilter(method='filter_host_os_type', choices=OSType.choices)       # Filter by host OS
    # Enumeration field names to use in the filters
    enumeration_fields: List[str] = []
    host_fields: List[str] = []                                                 # Host field names to use in the filters

    def filter_enumeration(self, queryset: QuerySet, name: str, value: int) -> QuerySet:
        '''Filter queryset by enumeration Id.

        Args:
            queryset (QuerySet): Finding queryset to be filtered
            name (str): Field name, not used in this case
            value (int): Enumeration Id

        Returns:
            QuerySet: Filtered queryset by enumeration Id
        '''
        return self.multiple_field_filter(queryset, value, self.enumeration_fields)

    def filter_enumeration_port(self, queryset: QuerySet, name: str, value: int) -> QuerySet:
        '''Filter queryset by enumeration port.

        Args:
            queryset (QuerySet): Finding queryset to be filtered
            name (str): Field name, not used in this case
            value (int): Enumeration port

        Returns:
            QuerySet: Filtered queryset by enumeration port
        '''
        return self.multiple_field_filter(queryset, value, [f'{f}__port' for f in self.enumeration_fields])

    def filter_host(self, queryset: QuerySet, name: str, value: int) -> QuerySet:
        '''Filter queryset by host Id.

        Args:
            queryset (QuerySet): Finding queryset to be filtered
            name (str): Field name, not used in this case
            value (int): Host Id

        Returns:
            QuerySet: Filtered queryset by host Id
        '''
        return self.multiple_field_filter(queryset, value, self.host_fields)

    def filter_host_address(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        '''Filter queryset by host address.

        Args:
            queryset (QuerySet): Finding queryset to be filtered
            name (str): Field name, not used in this case
            value (str): Host address

        Returns:
            QuerySet: Filtered queryset by host address
        '''
        return self.multiple_field_filter(queryset, value, [f'{f}__address' for f in self.host_fields])

    def filter_host_os_type(self, queryset: QuerySet, name: str, value: OSType) -> QuerySet:
        '''Filter queryset by host OS type.

        Args:
            queryset (QuerySet): Finding queryset to be filtered
            name (str): Field name, not used in this case
            value (OSType): OS type

        Returns:
            QuerySet: Filtered queryset by host OS type
        '''
        return self.multiple_field_filter(queryset, value, [f'{f}__os_type' for f in self.host_fields])


class OSINTFilter(FindingFilter):
    '''FilterSet to filter and sort OSINT entities.'''

    # Ordering fields including common ones
    o = OrderingFilter(fields=FINDING_ORDERING + ('data', 'data_type', 'source'))

    class Meta:
        '''FilterSet metadata.'''

        model = OSINT
        fields = FINDING_FILTERING.copy()                                       # Common filtering fields
        fields.update({                                                         # Include specific filtering fields
            'data': ['exact', 'icontains'],
            'data_type': ['exact'],
            'source': ['exact', 'icontains'],
        })


class HostFilter(FindingFilter):
    '''FilterSet to filter and sort Host entities.'''

    o = OrderingFilter(fields=FINDING_ORDERING + ('address', 'os_type'))        # Ordering fields including common ones

    class Meta:
        '''FilterSet metadata.'''

        model = Host
        fields = FINDING_FILTERING.copy()                                       # Common filtering fields
        fields.update({                                                         # Include specific filtering fields
            'address': ['exact', 'icontains'],
            'os_type': ['exact'],
        })


class EnumerationFilter(FindingFilter):
    '''FilterSet to filter and sort Enumeration entities.'''

    # Ordering fields including common ones
    o = OrderingFilter(fields=FINDING_ORDERING + (('host__os_type', 'os_type'), 'host', 'port', 'protocol', 'service'))

    class Meta:
        '''FilterSet metadata.'''

        model = Enumeration
        fields = FINDING_FILTERING.copy()                                       # Common filtering fields
        fields.update({                                                         # Include specific filtering fields
            'host': ['exact', 'isnull'],
            'host__address': ['exact', 'icontains'],
            'host__os_type': ['exact'],
            'port': ['exact'],
            'port_status': ['iexact'],
            'protocol': ['iexact'],
            'service': ['exact', 'icontains'],
        })


class EndpointFilter(FindingFilter):
    '''FilterSet to filter and sort Endpoint entities.'''

    # Ordering fields including common ones
    o = OrderingFilter(fields=FINDING_ORDERING + (('enumeration__host', 'host'), 'enumeration', 'endpoint', 'status'))

    class Meta:
        '''FilterSet metadata.'''

        model = Endpoint
        fields = FINDING_FILTERING.copy()                                       # Common filtering fields
        fields.update({                                                         # Include specific filtering fields
            'enumeration': ['exact', 'isnull'],
            'enumeration__host': ['exact'],
            'enumeration__host__address': ['exact', 'icontains'],
            'enumeration__host__os_type': ['exact'],
            'enumeration__port': ['exact'],
            'endpoint': ['exact', 'icontains'],
            'status': ['exact'],
        })


class TechnologyFilter(FindingFilter):
    '''FilterSet to filter and sort Technology entities.'''

    # Ordering fields including common ones
    o = OrderingFilter(fields=FINDING_ORDERING + (('enumeration__host', 'host'), 'enumeration', 'name', 'version'))

    class Meta:
        '''FilterSet metadata.'''

        model = Technology
        fields = FINDING_FILTERING.copy()                                       # Common filtering fields
        fields.update({                                                         # Include specific filtering fields
            'enumeration': ['exact', 'isnull'],
            'enumeration__host': ['exact'],
            'enumeration__host__address': ['exact', 'icontains'],
            'enumeration__host__os_type': ['exact'],
            'enumeration__port': ['exact'],
            'name': ['exact', 'icontains'],
            'version': ['exact', 'icontains'],
            'related_to': ['exact'],
        })


class CredentialFilter(FindingFilter):
    '''FilterSet to filter and sort Credential entities.'''

    o = OrderingFilter(fields=FINDING_ORDERING + ('email', 'username'))         # Ordering fields including common ones

    class Meta:
        '''FilterSet metadata.'''

        model = Credential
        fields = FINDING_FILTERING.copy()                                       # Common filtering fields
        fields.update({                                                         # Include specific filtering fields
            'technology': ['exact', 'isnull'],
            'technology__enumeration': ['exact', 'isnull'],
            'technology__enumeration__host': ['exact'],
            'technology__enumeration__host__address': ['exact', 'icontains'],
            'technology__enumeration__host__os_type': ['exact'],
            'technology__enumeration__port': ['exact'],
            'technology__name': ['exact', 'icontains'],
            'technology__version': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'username': ['exact', 'icontains'],
        })


class VulnerabilityFilter(BaseVulnerabilityFilter):
    '''FilterSet to filter and sort Vulnerability entities.'''

    # Enumeration field names to use in the filters
    enumeration_fields: List[str] = ['technology__enumeration', 'enumeration']
    # Host field names to use in the filters
    host_fields: List[str] = ['technology__enumeration__host', 'enumeration__host']
    # Ordering fields including common ones
    o = OrderingFilter(fields=FINDING_ORDERING + ('enumeration', 'technology', 'name', 'severity', 'cve'))

    class Meta:
        '''FilterSet metadata.'''

        model = Vulnerability
        fields = FINDING_FILTERING.copy()                                       # Common filtering fields
        fields.update({                                                         # Include specific filtering fields
            'enumeration': ['isnull'],
            'technology': ['exact', 'isnull'],
            'technology__name': ['exact', 'icontains'],
            'technology__version': ['exact', 'icontains'],
            'name': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'severity': ['exact'],
            'cve': ['exact', 'contains'],
            'exploit': ['isnull']
        })


class ExploitFilter(BaseVulnerabilityFilter):
    '''FilterSet to filter and sort Exploit entities.'''

    # Enumeration field names to use in the filters
    enumeration_fields: List[str] = [
        'technology__enumeration', 'vulnerability__enumeration',
        'vulnerability__technology__enumeration'
    ]
    # Host field names to use in the filters
    host_fields: List[str] = [
        'technology__enumeration__host', 'vulnerability__enumeration__host',
        'vulnerability__technology__enumeration__host'
    ]
    # Ordering fields including common ones
    o = OrderingFilter(fields=FINDING_ORDERING + ('vulnerability', 'technology', 'name'))

    class Meta:
        '''FilterSet metadata.'''

        model = Exploit
        fields = FINDING_FILTERING.copy()                                       # Common filtering fields
        fields.update({                                                         # Include specific filtering fields
            'vulnerability': ['exact', 'isnull'],
            'vulnerability__name': ['exact', 'icontains'],
            'vulnerability__severity': ['exact'],
            'vulnerability__cve': ['exact', 'contains'],
            'vulnerability__technology': ['exact'],
            'vulnerability__technology__name': ['exact', 'icontains'],
            'vulnerability__technology__version': ['exact', 'icontains'],
            'technology': ['exact', 'isnull'],
            'technology__name': ['exact', 'icontains'],
            'technology__version': ['exact', 'icontains'],
            'technology__enumeration': ['exact'],
            'technology__enumeration__host': ['exact'],
            'technology__enumeration__host__address': ['exact', 'icontains'],
            'technology__enumeration__host__os_type': ['exact'],
            'technology__enumeration__port': ['exact'],
            'name': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'reference': ['exact', 'icontains'],
            'checked': ['exact'],
        })
