import re
from collections import defaultdict
from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response


class TableDefView(object):
    def __init__(self, columns=None):
        if not isinstance(columns, list):
            raise TypeError("%s should be a list of column definitions")
        self._response = Response(columns)

    @property
    def response(self):
        return self._response


class QueryView(object):
    def __init__(self, query_set=None, serializer_class=None, query_params=None,
                 static_filter=None, static_exclude=None, static_order=None):
        if not isinstance(query_params, QueryParams):
            raise TypeError("%s not an instance of QueryParams" % query_params)
        if not isinstance(query_set, QuerySet):
            raise TypeError("%s not an instance of QuerySet" % query_set)
        if not issubclass(serializer_class, serializers.BaseSerializer):
            raise TypeError("%s not a subclass of BaseSerializer" % serializer_class)
        query = query_params.query
        if not query:
            self._response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            base = query_set
            records_total = base.count()
            filter_value = query['search']['value']
            filter_query = Q()
            exclude_query = Q()
            if static_filter:
                filter_query |= static_filter
            elif filter_value:
                filter_cols = []
                for col_index in query['columns']:
                    if query['columns'][col_index]['searchable']:
                        filter_cols.append(query['columns'][col_index]['name'])
                for col in filter_cols:
                    filter_query |= Q(**{"%s__icontains" % col: filter_value})
            if static_exclude:
                exclude_query |= static_exclude
            filtered = base.filter(filter_query).exclude(exclude_query)
            records_filtered = filtered.count()
            order_by_columns = list()
            if static_order:
                order_by_columns.append(static_order)
            else:
                for i in query['order']:
                    col_index = query['order'][i]['column']
                    col_name = query['columns'][col_index]['name']
                    if query['order'][i]['dir']:
                        order_by_columns.append("-%s" % col_name)
                    else:
                        order_by_columns.append(col_name)
            ordered = filtered.order_by(*order_by_columns)
            page_start = query['start']
            page_end = page_start + query['length']
            page = ordered[page_start:page_end]
            serializer = serializer_class(page, many=True, context={'request': query_params.request})
            data = serializer.data
            response = {
                'draw': query['draw'],
                'recordsTotal': records_total,
                'recordsFiltered': records_filtered,
                'data': data,
            }
            self._response = Response(response)

    @property
    def response(self):
        return self._response


class QueryParams(object):
    _param_re = re.compile(r'^(\w+)')
    _index_re = re.compile(r'\[(\w+)\]')

    def _column_dict(self):
        obj = {
            'data': None,
            'name': None,
            'searchable': None,
            'orderable': None,
            'search': {
                'value': None,
                'regex': None,
            }
        }
        return obj

    def __init__(self, request=None):
        if not isinstance(request, Request):
            raise TypeError("%s is not a Request object" % request)
        self._request = request
        self._dict = {
            'draw': None,
            'start': None,
            'length': None,
            'search': {
                'value': None,
                'regex': None,
            },
            'order': defaultdict(dict),
            'columns': defaultdict(self._column_dict)
        }
        for key in request.query_params:
            val = request.query_params[key]
            param = self._param_re.match(key).group(0)
            if param == '_':
                continue
            elif param in ['draw', 'start', 'length']:
                self._dict[param] = int(val)
            elif param in ['search']:
                index = self._index_re.search(key).group(1)
                if index == 'value':
                    self._dict[param][index] = str(val)
                elif index == 'regex':
                    self._dict[param][index] = bool(val)
                else:
                    raise ValueError("Couldn't parse key %s" % key)
            elif param in ['order', 'columns']:
                indices = self._index_re.findall(key)
                i = int(indices[0])
                if param == 'order':
                    if indices[1] == 'column':
                        self._dict[param][i][indices[1]] = int(val)
                    elif indices[1] == 'dir':
                        if val == 'asc':
                            self._dict[param][i][indices[1]] = 0
                        elif val == 'desc':
                            self._dict[param][i][indices[1]] = 1
                        else:
                            raise ValueError("Couldn't parse key %s" % key)
                    else:
                        raise ValueError("Couldn't parse key %s" % key)
                elif param == 'columns':
                    if indices[1] in ['data', 'name']:
                        self._dict[param][i][indices[1]] = str(val)
                    elif indices[1] in ['searchable', 'orderable']:
                        if val == "true":
                            self._dict[param][i][indices[1]] = True
                        elif val == "false":
                            self._dict[param][i][indices[1]] = False
                        else:
                            raise ValueError("Couldn't parse key %s" % key)
                    elif indices[1] == 'search':
                        if indices[2] == 'value':
                            self._dict[param][i][indices[1]][indices[2]] = str(val)
                        elif indices[2] == 'regex':
                            self._dict[param][i][indices[1]][indices[2]] = bool(val)
                        else:
                            raise ValueError("Couldn't parse key %s" % key)
                    else:
                        raise ValueError("Couldn't parse key %s" % key)
                else:
                    raise ValueError("Couldn't parse key %s" % key)
            else:
                raise ValueError("Couldn't parse key %s" % key)

    @property
    def query(self):
        return self._dict

    @property
    def request(self):
        return self._request
