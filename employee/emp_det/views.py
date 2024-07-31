from rest_framework import generics, status
from .models import Employee, Project
from .serializers import EmployeeSerializer, ProjectSerializer, EmployeeGetSerializer, ProjectGetSerializer
from rest_framework import status
from rest_framework.response import Response
import logging

from rest_framework.permissions import IsAuthenticated
from emp_det.authentication import CustomAuthentication

logger = logging.getLogger(__name__)

class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    """
    View for listing and creating employees.

    This view inherits from `generics.ListCreateAPIView` and is responsible for handling GET and POST requests for employee data.

    Attributes:
        queryset (QuerySet): A QuerySet of all active employees.
        serializer_class (Serializer): The serializer class used for this view.
        authentication_classes (List[AuthenticationClass]): A list of authentication classes that are checked in order.
        permission_classes (List[PermissionClass]): A list of permission classes that are checked in order.

    Methods:
        get_queryset(self):
            Returns a QuerySet of all employees.

        list(self, request, *args, **kwargs):
            Handles GET requests. If no employees are found, returns a 404 response with a message. Otherwise, serializes the queryset and returns the serialized data in the response.

        get_serializer_class(self):
            Returns the appropriate serializer class based on the request method.

        create(self, request, *args, **kwargs):
            Handles POST requests. Validates the incoming request data and saves it using the serializer. Returns a response with the created data or validation errors.
    """
    # queryset = Employee.objects.all()
    queryset = Employee.objects.filter(active=True)
    
    serializer_class = EmployeeSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves a QuerySet of all employees from the database and returns the serialized data in the  response.

        Parameters:
        self (EmployeeListCreateAPIView instance): An instance of the EmployeeListCreateAPIView class.

        Returns:
        QuerySet: A QuerySet of all employees from the database whose staturs is active.

        Raises:
        None

        Example:
        >>> queryset = get_queryset(self)
        >>> print(queryset)
        """
        queryset = Employee.objects.filter(active=True)
        self.emp_found = not queryset.exists()
        logger.info("(get_queryset)queryset: %s", queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Handles GET requests for employee data.

        This method is responsible for fetching a QuerySet of all employees from the database and returning the serialized  data in the response.

        Parameters:
        request (HttpRequest): The HTTP request object.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

        Returns:
        Response: A HTTP response containing the serialized data of the employees.

        Raises:
        None

        Example:
        >>> response = list(self, request, *args, **kwargs)
        >>> print(response.data)
        """
        queryset = self.get_queryset()

        if self.emp_found:
            return Response({"detail": "No employees found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        logger.info("(list)queryset: %s", queryset)
        return Response(serializer.data)

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the request method.
    
        This method is responsible for determining the appropriate serializer class to use for the given request.
    
        Parameters:
        self (EmployeeListCreateAPIView instance): An instance of the EmployeeListCreateAPIView class.
    
        Returns:
        SerializerClass: A subclass of `rest_framework.serializers.Serializer` that is appropriate for the given request method.
    
        Raises:
        None
    
        Example:
        >>> serializer_class = get_serializer_class(self)
        >>> print(serializer_class)
        """
        if self.request.method == 'GET':
            return EmployeeGetSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        Handles POST requests for creating a new employee.

        This method is responsible for validating the incoming request data and saving it using the serializer.
        If the serializer is valid, it performs the create operation and returns a response with the created data and   appropriate HTTP status code.
        If the serializer is not valid, it returns a response with the validation errors and an HTTP status code of 400     (Bad Request).

        Parameters:
        request (HttpRequest): The HTTP request object containing the data for the new employee.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

        Returns:
        Response: A HTTP response containing the serialized data of the newly created employee or validation errors.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting employees.

    This view inherits from `generics.RetrieveUpdateDestroyAPIView` and is responsible for handling GET, PUT, and DELETE requests for employee data.

    Attributes:
        queryset (QuerySet): A QuerySet of all active employees.
        serializer_class (Serializer): The serializer class used for this view.
        lookup_field (str): The field used to lookup the employee in the queryset. Defaults to 'pk'.
        authentication_classes (List[AuthenticationClass]): A list of authentication classes that are checked in order.
        permission_classes (List[PermissionClass]): A list of permission classes that are checked in order.

    Methods:
        get_object(self, *args, **kwargs):
            Retrieves a single employee instance from the queryset based on the provided primary key.

        retrieve(self, request, *args, **kwargs):
            Handles GET requests. If an employee is found, it serializes the employee instance and returns the serialized data in the response.

        update(self, request, *args, **kwargs):
            Handles PUT requests. Validates the incoming request data and updates the employee instance using the serializer. Returns a response with the updated data or validation errors.

        partial_update(self, request, *args, **kwargs):
            Handles PATCH requests. Validates the incoming request data and updates the employee instance using the serializer. Returns a response with the updated data or validation errors.

        destroy(self, request, *args, **kwargs):
            Handles DELETE requests. If an employee is found, it deletes the employee instance and returns a 204 No Content response.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    """
    View for listing and creating projects.

    This view inherits from `generics.ListCreateAPIView` and is responsible for handling GET and POST requests for project data.

    Attributes:
        queryset (QuerySet): A QuerySet of all projects.
        serializer_class (Serializer): The serializer class used for this view.
        authentication_classes (List[AuthenticationClass]): A list of authentication classes that are checked in order.
        permission_classes (List[PermissionClass]): A list of permission classes that are checked in order.

    Methods:
        get_serializer_class(self):
            Returns the appropriate serializer class based on the request method.

        If the request method is GET, it returns the `ProjectGetSerializer` class. Otherwise, it returns the `ProjectSerializer` class.

    Returns:
        SerializerClass: A subclass of `rest_framework.serializers.Serializer` that is appropriate for the given request method.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the request method.

        This method is responsible for determining the appropriate serializer class to use for the  given request.

        Parameters:
        self (ProjectListCreateAPIView instance): An instance of the ProjectListCreateAPIView   class.

        Returns:
        SerializerClass: A subclass of `rest_framework.serializers.Serializer` that is appropriate  for the given request method.

        If the request method is GET, it returns the `ProjectGetSerializer` class. Otherwise, it    returns the `ProjectSerializer` class.
        """
        if self.request.method == 'GET':
            return ProjectGetSerializer
        return super().get_serializer_class()


class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting projects.

    This view inherits from `generics.RetrieveUpdateDestroyAPIView` and is responsible for handling GET, PUT, and DELETE requests for project data.

    Attributes:
        queryset (QuerySet): A QuerySet of all projects.
        serializer_class (Serializer): The serializer class used for this view.
        lookup_field (str): The field used to lookup the project in the queryset. Defaults to 'pk'.
        authentication_classes (List[AuthenticationClass]): A list of authentication classes that are checked in order.
        permission_classes (List[PermissionClass]): A list of permission classes that are checked in order.

    Methods:
        get_object(self, *args, **kwargs):
            Retrieves a single project instance from the queryset based on the provided primary key.

        retrieve(self, request, *args, **kwargs):
            Handles GET requests. If a project is found, it serializes the project instance and returns the serialized data in the response.

        update(self, request, *args, **kwargs):
            Handles PUT requests. Validates the incoming request data and updates the project instance using the serializer. Returns a response with the updated data or validation errors.

        partial_update(self, request, *args, **kwargs):
            Handles PATCH requests. Validates the incoming request data and updates the project instance using the serializer. Returns a response with the updated data or validation errors.

        destroy(self, request, *args, **kwargs):
            Handles DELETE requests. If a project is found, it deletes the project instance and returns a 204 No Content response.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'pk'
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]