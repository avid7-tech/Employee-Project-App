from rest_framework import generics, status
from .models import Employee, Project
from .serializers import EmployeeSerializer, ProjectSerializer, EmployeeGetSerializer, ProjectGetSerializer
from rest_framework import status
from rest_framework.response import Response
import logging
# from rest_framework.permissions import IsAuthenticated
# from emp_det.authentication import CustomAuthentication
from django.http import JsonResponse

from openpyxl import Workbook
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import redirect


logger = logging.getLogger(__name__)

class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user =  request.user
        auth = request.auth
        
        logger.info("request user: %s", user)
        logger.info("request auth: %s", auth)
        
        # if not user.is_authenticated:
        #     logger.warning("Unauthenticated access attempt by user: %s", user)
        #     return self.handle_unauthenticated_user(request)
        
        return self.list(request, *args, **kwargs)

    # def handle_unauthenticated_user(self, request):
    #     return JsonResponse({'detail': 'Authentication required'}, status=401)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if self.emp_found:
            return Response({"detail": "No employees found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        # logger.info("(list)queryset: %s", queryset)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Employee.objects.filter(active=True)
        self.emp_found = not queryset.exists()
        # logger.info("(get_queryset)queryset: %s", queryset)
        return queryset

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        # kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmployeeGetSerializer
        elif self.request.method == 'POST':
            return EmployeeSerializer
        return super().get_serializer_class()
    
    def post(self, request, *args, **kwargs):
        logger.info(f"POST request data: {request.data}")   
        
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perfrom_create(self, serializer):
        serializer.save(user = self.request.user)


class EmployeeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectGetSerializer
        return super().get_serializer_class()


class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'pk'
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [IsAuthenticated]


class EmployeeReportAPIView(APIView):
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        wb = Workbook()
        ws = wb.active
        ws.title = "Employee Report"

        headers = ["Name", "Role", "Company", "Phone", "Active", "Project Title", "Project Status"]
        ws.append(headers)
        
        employees = Employee.objects.prefetch_related('projects').all()
        
        for employee in employees:
            phones = ", ".join(employee.phone) if isinstance(employee.phone, list) else ""

            if employee.projects.exists():
                for project in employee.projects.all():
                    ws.append([
                        employee.name,
                        employee.role,
                        employee.company,
                        phones,
                        employee.active,
                        project.title,
                        project.status
                    ])
            else:
                ws.append([
                    employee.name,
                    employee.role,
                    employee.company,
                    phones,
                    employee.active,
                ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=employee_report.xlsx'
        wb.save(response)
        
        return response

class RedirectToEmployeeListView(APIView):
    def get(self, request, *args, **kwargs):
        return redirect('employee-list-create')
