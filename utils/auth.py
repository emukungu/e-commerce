import jwt

from django.conf import settings

from rest_framework import authentication, exceptions


def decode_token(self, request):

  auth_header = authentication.get_authorization_header(request).split( )
  token = auth_header[1].decode('utf-8')

  payload = jwt.decode(token, settings.SECRET_KEY)

  return payload
    


