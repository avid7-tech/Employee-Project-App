from rest_framework import generics, status
from .models import Employee, Project
from .serializers import EmployeeSerializer, ProjectSerializer
from rest_framework import status
from rest_framework.response import Response
import logging
from collections import Counter
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [BasicAuthentication]
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
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]



class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
        
    #     expected_fields = set(serializer.fields.keys()) - {'id'}
    #     provided_fields = set(request.data.keys())
        
    #     logger.info(f"expected: {expected_fields}")
    #     logger.info(f"provided: {provided_fields}")
        
    #     if expected_fields!= provided_fields or len(expected_fields)!= len(provided_fields):
    #         return Response(
    #             {"error": "The fields in the request do not match the expected fields or contain duplicates."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
        
    #     if serializer.is_valid():
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'pk'
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
