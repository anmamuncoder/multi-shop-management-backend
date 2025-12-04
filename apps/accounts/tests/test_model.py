import pytest
from apps.accounts.models import User
from django.db import IntegrityError
from .factories import UserFactory

pytestmark = pytest.mark.django_db

# ---------------------------
# Pytest Fixture
# ---------------------------
@pytest.fixture
def user():
    """Demo User create with role base customer and shop_owner"""
    customer = UserFactory()
    shop_owner = UserFactory()
    return customer, shop_owner
 

# ---------------------------
# Test Model
# ---------------------------
def test_create_user(user):
    """
    Test that for creating user properly and after then username auto add the email name
    """
    
    user = User.objects.create(email='test@example.com',role='customer')
    user.set_password("testPassword123")
    user.save()
    
    user.refresh_from_db()
    
    assert user.username == 'test'
    assert user.email == "test@example.com"
    assert user.email_verified == False
    assert str(user) == user.email
 
def test_unique_email(user):
    """
    Test that check unique email working properly
    """
    user = User.objects.create(email='test@example.com',role='customer')
    user.set_password("testPassword123")
    user.save()

    user.refresh_from_db()

    with pytest.raises(IntegrityError):
        user1 = User.objects.create(email='test@example.com',role='customer')
     
