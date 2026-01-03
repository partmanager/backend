import json
from django.http import JsonResponse
from .models.part import Part


menu = {
    'id': 500,
    'label': 'Root',
    'selectable': False,
    'children': [
        {
            'id': 501,
            'label': "Mechanical",
            'selectable': False,
            'children': [
                {
                    'id': 505,
                    'label': "Bearings",
                    'selectable': False,
                    'children': []
                },
                {
                    'id': 505,
                    'label': "Bolts",
                    'selectable': False,
                    'children': []
                },
                {
                    'id': 506,
                    'label': "Nuts",
                    'selectable': False,
                    'children': []
                },
            ]
        },
        {
            'id': 502,
            'label': "Elecromechanical",
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
    ]
}


def get_part_menu(request):
    return JsonResponse(menu)

