##Functionalities:

### Custom Middleware

1. **AuthenticationMiddleware**
   - **Purpose**: Provides custom authentication handling and logs request details.
   - **Functionality**:
     - Logs request method and URL.
     - Extracts and validates credentials from request headers.
     - Uses Basic Authentication scheme.
     - Logs authentication success or failure.

2. **RequestLoggingMiddleware**
   - **Purpose**: Logs incoming request details for debugging and monitoring.
   - **Functionality**:
     - Logs request method, URL, and headers.
     - Optionally logs request body.

3. **ResponseLoggingMiddleware**
   - **Purpose**: Logs outgoing response details.
   - **Functionality**:
     - Logs response status code and body.
     - Useful for debugging and monitoring responses.

4. **ErrorHandlingMiddleware**
   - **Purpose**: Handles and logs errors occurring during request processing.
   - **Functionality**:
     - Captures exceptions and logs error details.
     - Returns a custom error response format.

### API Endpoints
- **EmployeeListCreateAPIView**
  - **GET**: Lists all active employees.
  - **POST**: Creates a new employee.

- **EmployeeRetrieveUpdateDestroyAPIView**
  - **GET**: Retrieves a specific employee by ID.
  - **PUT**: Updates a specific employee by ID.
  - **PATCH**: Partially updates a specific employee by ID.
  - **DELETE**: Deletes a specific employee by ID.

- **ProjectListCreateAPIView**
  - **GET**: Lists all projects.
  - **POST**: Creates a new project.

- **ProjectRetrieveUpdateDestroyAPIView**
  - **GET**: Retrieves a specific project by ID.
  - **PUT**: Updates a specific project by ID.
  - **PATCH**: Partially updates a specific project by ID.
  - **DELETE**: Deletes a specific project by ID.

### Serializers
- **EmployeeSerializer**
  - Validates name, phone numbers, company, and role.
  - Checks for uniqueness of name and phone number.
  - Validates if all required fields are provided.

- **EmployeeGetSerializer**
  - Includes fields: name, address, role, phone, company.
  - Computes and includes project count, ongoing project count, and completed project count.

- **ProjectSerializer**
  - Validates title.
  - Ensures end date is after the start date and computes duration.

- **ProjectGetSerializer**
  - Includes fields: title, description, start date, end date, status.

### Models
- **Employee Model**
  - Fields: name, phone, company, role, active, address.
  - Contains unique name validation and related projects.

- **Project Model**
  - Fields: title, description, start date, end date, duration, employee, status.
  - Validates end date is after start date.

- **Address Model**
  - Fields: add_line, state, hometown, pincode.
  - Validates pincode length and state format.

This summary now includes custom middleware functionalities, along with other details of your project.