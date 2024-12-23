import io

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Project, ProjectVersion, BOM, BOMItem, Assembly, AssemblyItem, AssemblyJob, Rework
from .serializers import \
    AssemblySerializer, AssemblyJobSerializer, \
    BOMSerializer, BOMDetailSerializer, BOMUpdateSerializer, \
    BOMItemSerializer, BOMItemUpdateSerializer, BOMItemCreateSerializer, \
    ProjectSerializer, ProjectDetailSerializer, ProjectVersionSerializer, ProjectVersionDetailSerializer, \
    ProjectVersionCreateSerializer, AssemblyJobCreateSerializer, AssemblyItemSerializer, AssemblyItemCreateSerializer, ReworkSerializer
from .forms import BOMImportForm
from .BomImporter import CircuitStudioImporter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.views.generic import FormView
from .tasks import close_rework


def projects_menu(request):
    projects = []
    for project in Project.objects.all():
        project_versions = []
        for project_version in project.projectversion_set.all():
            boms = []
            for bom in project_version.bom_set.all():
                boms.append({'id': f"bom/{bom.pk}",
                             'label': bom.name,
                             'selectable': True,
                             'children': []})
            assemblies = []
            for assembly in project_version.assembly_set.all():
                assemblies.append({'id': f"assembly/{assembly.pk}",
                                   'label': assembly.name,
                                   'selectable': True,
                                   'children': []})

            project_versions.append({'id': project_version.pk,
                                     'label': project_version.name,
                                     'selectable': True,
                                     'children': [{'id': f"{project_version.pk}-boms",
                                                   'label': 'BOMs',
                                                   'selectable': False,
                                                   'children': boms},
                                                  {'id': f"{project_version.pk}-assemblies",
                                                   'label': 'assemblies',
                                                   'selectable': False,
                                                   'children': assemblies}]})
        projects.append({'id': f"project-{project.pk}",
                         'label': project.name,
                         'selectable': False,
                         'children': project_versions
                         })

    menu = {'id': None,
            'label': 'Projects',
            'selectable': False,
            'children': projects
            }

    return JsonResponse(menu)


class AssemblyViewSet(ModelViewSet):
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project_version']


class AssemblyItemViewSet(ModelViewSet):
    queryset = AssemblyItem.objects.all()
    serializer_class = AssemblyItemSerializer
    search_fields = ['designator', 'part__manufacturer_part_number']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['assembly', 'rework', 'assembly__assembly_job']

    def get_serializer_class(self):
        if self.action == 'create':
            return AssemblyItemCreateSerializer
        return AssemblyItemSerializer


class AssemblyJobViewSet(ModelViewSet):
    queryset = AssemblyJob.objects.all()
    serializer_class = AssemblyJobSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project_version']

    def get_serializer_class(self):
        if self.action == 'create':
            return AssemblyJobCreateSerializer
        return AssemblyJobSerializer


class ReworkViewSet(ModelViewSet):
    queryset = Rework.objects.all()
    serializer_class = ReworkSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assembly']


class BOMViewSet(ModelViewSet):
    queryset = BOM.objects.all()
    serializer_class = BOMSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BOMDetailSerializer
        elif self.action == 'update':
            return BOMUpdateSerializer
        return BOMSerializer


class BOMItemViewSet(ModelViewSet):
    queryset = BOMItem.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return BOMItemUpdateSerializer
        elif self.action == 'create':
            return BOMItemCreateSerializer
        return BOMItemSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer


class ProjectVersionViewSet(ModelViewSet):
    queryset = ProjectVersion.objects.all()
    serializer_class = ProjectVersionSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectVersionDetailSerializer
        elif self.action == 'create':
            return ProjectVersionCreateSerializer
        return ProjectVersionSerializer


class GenerateAssemblyViewSet(APIView):
    def post(self, request, pk):
        assembly_job = AssemblyJob.objects.get(pk=pk)
        assembly_job.generate_from_bom()
        return Response('')


class CloseReworkViewSet(APIView):
    def post(self, request, pk):
        close_rework(pk)
        return Response('')


class BOMImportView(FormView):
    form_class = BOMImportForm

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # if self.request.accepts('text/html'):
        #    return response
        # else:
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        bom_import_file = form.cleaned_data['bom_file']

        bom = BOM(name=form.cleaned_data['name'],
                  description=form.cleaned_data['description'],
                  multiply=form.cleaned_data['multiply'],
                  project=form.cleaned_data['project'])
        bom.save()

        f = io.StringIO(bom_import_file.read().decode(encoding='windows-1252'))
        CircuitStudioImporter.process_bom_from_file(f, bom)

        # response = super().form_valid(form)
        # if result_invoice_model is not None:
        return JsonResponse({'status': 'success'})  # response
        # else:
        #    return JsonResponse({'status': 'Error'})
