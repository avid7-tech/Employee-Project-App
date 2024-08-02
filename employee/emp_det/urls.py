from django.urls import path
from .views import (
    EmployeeListCreateAPIView,
    EmployeeRetrieveUpdateDestroyAPIView,
    ProjectListCreateAPIView,
    ProjectRetrieveUpdateDestroyAPIView,
    EmployeeReportAPIView,
    RedirectToEmployeeListView
)
from rest_framework_simplejwt.views import(
TokenObtainPairView,
TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/employees/', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
    path('api/employees/<int:pk>/', EmployeeRetrieveUpdateDestroyAPIView.as_view(), name='employee-retrieve-update-destroy'),
    path('api/projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('api/projects/<int:pk>/', ProjectRetrieveUpdateDestroyAPIView.as_view(), name='project-retrieve-update-destroy'),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('api/employees/reports/', EmployeeReportAPIView.as_view(), name='employee-report'),
    path('api/employees/redirect/', RedirectToEmployeeListView.as_view(), name='redirect_to_employee_list'),
]
