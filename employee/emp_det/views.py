from rest_framework import generics, status
from .models import Employee, Project
from .serializers import EmployeeSerializer, ProjectSerializer
from rest_framework import status
from rest_framework.response import Response
import logging

from rest_framework.permissions import IsAuthenticated
from emp_det.authentication import CustomAuthentication

logger = logging.getLogger(__name__)


class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    
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
