import json
from django.http import JsonResponse
from .models.part import Part
from .tasks import import_components

menu = {'id': 500,
        'label': 'Root',
        'selectable': False,
        'children': [
            {'id': 100,
             'label': "Passives",
             'selectable': False,
             'children': [{'id': 15, 'label': "Balun", 'path': "/parts/15"},
                          {'id': 0, 'label': "Resistors", 'path': "/parts/0"},
                          {'id': 1, 'label': "Capacitors", 'path': "/parts/1"},
                          {'id': 2, 'label': "Inductors", 'path': "/parts/2"},
                          {'id': 8, 'label': "Ferrite Bead", 'path': "/parts/8"}]
             },
            {'id': 200,
             'label': "Diodes",
             'selectable': False,
             'children': [
                 {'id': 3,
                  'label': "Small signal",
                  'path': "/parts/3"
                  },
                 {'id': 4,
                  'label': "LED",
                  'path': "/parts/4"
                  },
                 {'id': 17,
                  'label': "Bridge Rectifiers",
                  'path': "/parts/17"
                  }
             ]
             },
            {'id': 5,
             'label': "TVS",
             'path': "/parts/5"
             },
            {'id': 9,
             'label': "Cristal",
             'path': "/parts/9"
             },
            {'id': 6,
             'label': "Transistor Bipolar",
             'path': "/parts/6"
             },
            {'id': 18,
             'label': "Transistor Mosfet",
             'path': "/parts/18"
             },
            {'id': 7,
             'label': "Integrated Circuits",
             'path': "/parts/7"},
            {'id': 300,
             'label': "Connectors",
             'selectable': False,
             'children': [
                 {'id': 10,
                  'label': "Connector",
                  'path': "/parts/10"
                  }
             ]
             },
            {'id': 11,
             'label': "Modules",
             'path': "/parts/11"},
            {'id': 12,
             'label': "Enclosures",
             'path': "/parts/12"},
            {'id': 16,
             'label': "Battery",
             'path': "/parts/16"},
            {'id': 13,
             'label': "Battery Holders",
             'path': "/parts/13"},
            {'id': 14,
             'label': "Switch",
             'path': 'parts/14'
             }
        ]
        }


def get_part_menu(request):
    return JsonResponse(menu)


def get_part_detail(request):
    data = json.loads(request.body.decode("utf-8"))
    if data and 'id' in data:
        pk = data['id']
        part = Part.objects.filter(pk=pk).get()
        print(part)
        queryset = __get_part_type_queryset(part.part_type)
        print(queryset)
        queryset = queryset.filter(part_ptr_id=pk)

        generic_parameters = {
            'mpn': part.manufacturer_part_number,
            'description': part.description,
            'manufacturer': part.manufacturer.name,
            'production_status': part.production_status,
            'notes': part.notes,
            'comment': part.comment,
            'storage_conditions': part.storage_conditions.to_ajax(),
            'operating_conditions': None,
        }

        manufacturer_order_numbers = []
        for mon in part.manufacturer_order_number_set.all():
            manufacturer_order_numbers.extend(mon.to_ajax_response())

        response = {
            'product_url': part.product_url,
            'generic_parameters': generic_parameters,
            'distributors': part.distributor_pk_set(),
            'manufacturer_order_numbers': manufacturer_order_numbers,
            'package': part.package.to_ajax() if part.package else None,
            'symbol': part.symbol.to_ajax() if part.symbol else None,
            'files': part.get_files_array()
        }
        print(response)
        return JsonResponse({'data': response})


def start_import(request):
    import_components.delay()
    response = {"total": True
                }
    return JsonResponse(response, safe=False)
