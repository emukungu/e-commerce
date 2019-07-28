import jwt

from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User

class JWTAuthentication(authentication.BaseAuthentication):

  def authenticate(self, request):
    try:
      auth_header = authentication.get_authorization_header(request).split()

      if not auth_header:
        return None

      token = auth_header[1].decode('utf-8')

      payload = jwt.decode(token, settings.SECRET_KEY)
    except:
      msg = 'Invalid authetication. Could not decode token.'
      raise exceptions.AuthenticationFailed(msg)
    try:
      user = User.objects.get(pk = payload['id'])
    except:
      msg = 'No user matching this token exists.'
      raise exceptions.AuthenticationFailed(msg)
    if not user.is_active:
      msg = 'User has been deactivated.'
      raise exceptions.AuthenticationFailed(msg)

    return (user, token)
