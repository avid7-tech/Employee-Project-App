from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import logging
from django.contrib.auth.models import User
import base64
from django.contrib.auth.hashers import check_password

logger = logging.getLogger(__name__)

class CustomAuthentication(BaseAuthentication):
    """
    Custom authentication class that authenticates users based on HTTP Basic Authentication scheme.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        Tuple[User, None]: A tuple containing the authenticated User object and None if the authentication is successful.
        Raises:
            AuthenticationFailed: If the username or password is invalid.

    The function first checks if the request contains the 'Authorization' header. If it does, it decodes the credentials using base64. If the decoded credentials are provided, it splits them into username and password. If the username is not provided and the decoded credentials are present, it extracts the username and password from them.

    If a username is not provided, it logs a warning and returns None. It then checks if the username is provided and if the provided credentials match with the ones stored in the database. If the credentials match, it logs an info message and returns a tuple containing the authenticated User object and None. If the credentials do not match, it logs a warning message and raises an AuthenticationFailed exception with an appropriate error message.
    """
    def authenticate(self, request):
        logger.info("(authentication)Request Incoming: %s %s", request.method, request.get_full_path())
        logger.info("(authentication)Request Headers: %s", dict(request.headers))

        code = request.headers.get('Authorization')
        logger.info("(authentication)Request code: %s", code)

        decoded_credentials = None
        
        if code:
            code_one, code_two = code.split(' ')
            if code_one.lower() == 'basic':
                decoded_credentials = base64.b64decode(code_two).decode('utf-8')
                logger.info("(authentication)Decoded code: %s", decoded_credentials)

        username = request.GET.get('username') or request.data.get('username')
        if not username and decoded_credentials:
            username = decoded_credentials.split(':')[0]
            password = decoded_credentials.split(':')[1]
        
        
        if not username:
            logger.warning("No username provided in the request (authentication)")
            return None
        
        # details to check
        logger.info("to check username: %s", username)
        logger.info("to check password: %s", password)
        
        if not username:
            logger.warning("No username provided in the request (authentication)")
            return None

        
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            logger.info("Authentication successful (authentication)")
            return (user, None)
        else:
            logger.warning("Password does not match (authentication)")
            raise AuthenticationFailed("Invalid username or password (authentication)")
