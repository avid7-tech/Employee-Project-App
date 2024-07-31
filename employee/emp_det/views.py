from rest_framework import generics, status
from .models import Employee, Project
from .serializers import EmployeeSerializer, ProjectSerializer, EmployeeGetSerializer
from rest_framework import status
from rest_framework.response import Response
import logging

from rest_framework.permissions import IsAuthenticated
from emp_det.authentication import CustomAuthentication

logger = logging.getLogger(__name__)

class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    # queryset = Employee.objects.all()
    queryset = Employee.objects.filter(active=True)
    
    serializer_class = EmployeeSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Employee.objects.all()
        # queryset = Employee.objects.filter(role="admin")
        self.emp_found = not queryset.exists()
        logger.info("(get_queryset)queryset: %s", queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if self.emp_found:
            return Response({"detail": "No employees found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        logger.info("(list)queryset: %s", queryset)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmployeeGetSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]



class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]


class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'pk'
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

"""
Initialization:

EmployeeListCreateAPIView is initialized with its default queryset and serializer.
GET Request Handling:

list method is called.
get_queryset method is invoked to fetch the queryset.
If no records are found (emp_found is True), a 404 response is returned with a message.
Otherwise, the queryset is serialized using the appropriate serializer and returned in the response.
POST Request Handling:

create method is called.
The incoming request data is validated and saved using the serializer.
A response is returned with the created data or validation errors.

"""
