import base64
import logging
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

logger = logging.getLogger(__name__)

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info("Request Incoming: %s %s", request.method, request.get_full_path())
        logger.info("Request Headers: %s", dict(request.headers))
        
        code = request.headers.get('Authorization')
        logger.info("code: %s", code)
        if code:
            code_one, code_two = code.split(' ')
            if code_one.lower() == 'basic':
                decoded_credentials = base64.b64decode(code_two).decode('utf-8')
                username, password = decoded_credentials.split(':', 1)
                
                
                User = get_user_model()
                try:
                    user = User.objects.get(username=username)
                    if not check_password(password, user.password):
                        logger.info("password did not match (middleware check)")
                        return JsonResponse({'detail': 'Invalid username or password (middleware check)'}, status=401)
                    else:
                        logger.info("password matched (middleware check)")
                except User.DoesNotExist:
                    logger.info("user does not exist (middleware check)")
                    return JsonResponse({'detail': 'Invalid username or password (middleware check)'}, status=401)

        response = self.get_response(request)
        return response
