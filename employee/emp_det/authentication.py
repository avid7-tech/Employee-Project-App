from rest_framework.authentication import BaseAuthentication, get_authorization_header, authenticate, get_user_model
import base64
import binascii
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User


class CustomAuthentication(BaseAuthentication):
    """
    HTTP Basic authentication against username/password.
    """
    www_authenticate_realm = 'api'
    
    def authenticate_credentials(self, userid, password, request=None):
        """
        Authenticate the userid and password against username and password
        with optional request for context.
        """
        credentials = {
            get_user_model().USERNAME_FIELD: userid,
            'password': password
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (user, None)

    def authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            try:
                auth_decoded = base64.b64decode(auth[1]).decode('utf-8')
            except UnicodeDecodeError:
                auth_decoded = base64.b64decode(auth[1]).decode('latin-1')

            userid, password = auth_decoded.split(':', 1)
        except (TypeError, ValueError, UnicodeDecodeError, binascii.Error):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(userid, password, request)

# Client -> Webserver -> WSGI -> Request(middleware) -> url resolution -> view (middleware) -> view -> Exception(middleware) -> Response(middleware) -> WSGI -> WebServer -> Client
