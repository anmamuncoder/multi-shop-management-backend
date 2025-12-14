# Library
import factory
# Internal
from apps.accounts.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User 
    username = factory.Sequence(lambda n: f"user {n}")
    email = factory.Sequence(lambda n: f"user{n}@gmail.com")
    password = factory.PostGenerationMethodCall('set_password','TestPassword123')
    role = factory.Iterator(['customer','shop_owner'])
