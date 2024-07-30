from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import logging
from django.contrib.auth.models import User
import base64
from django.contrib.auth.hashers import check_password

logger = logging.getLogger(__name__)

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        logger.info("Request Incoming: %s %s", request.method, request.get_full_path())
        logger.info("Request Headers: %s", dict(request.headers))

        code = request.headers.get('Authorization')
        logger.info("Request code: %s", code)

        decoded_credentials = None
        
        if code:
            code_one, code_two = code.split(' ')
            if code_one.lower() == 'basic':
                decoded_credentials = base64.b64decode(code_two).decode('utf-8')
                logger.info("Decoded code: %s", decoded_credentials)

        username = request.GET.get('username') or request.data.get('username')
        if not username and decoded_credentials:
            username = decoded_credentials.split(':')[0]
            password = decoded_credentials.split(':')[1]
        
        
        if not username:
            logger.warning("No username provided in the request")
            return None
        
        # details to check
        logger.info("to check username: %s", username)
        logger.info("to check password: %s", password)
        
        if not username:
            logger.warning("No username provided in the request")
            return None

        
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            logger.info("Authentication successful")
            return (user, None)
        else:
            logger.warning("Password does not match")
            raise AuthenticationFailed("Invalid username or password")
