import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
  AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
  
  def create_user(self, username, email, password=None):
    """Create and return a user """
    if username is None:
      raise TypeError('username can not be empty')
    
    if email is None:
      raise TypeError('email can not be empty')
    
    email = self.normalize_email(email)
    user = self.model(username= username, email = email)
    user.set_password(password)

    user.save(using= self._db)
    return user
    
  
  def create_superuser(self, username, email, password):
    """Create a super user wit admin permissions """

    if password is None:
      raise ValueError('Password can not be empty.')

    user = self.create_user(username, email, password)
    user.is_superuser = True
    user.is_admin = True
    user.is_staff = True

    user.save(using= self._db) #use te same db that we created with the user profile manager
    return user


class User(AbstractBaseUser, PermissionsMixin):

  username = models.CharField(max_length=255, unique=True)
  email = models.EmailField(max_length=255, unique=True)
  is_active = models.BooleanField(default = True)
  is_staff = models.BooleanField(default = False)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  objects = UserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  def __str__(self):
    return self.username

  @property
  def token(self):
    return self.generate_jwt_token()
    
  # add jwt token

  def generate_jwt_token(self):

    expiry_date = datetime.now() + timedelta(days = 60)
    token = jwt.encode({
      'id': self.pk,
      'username': self.username,
      'exp': int(expiry_date.strftime('%s'))
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')




