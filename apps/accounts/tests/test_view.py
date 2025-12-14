import pytest
from rest_framework import status
from rest_framework.test import APIClient
from .factories import UserFactory
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

pytestmark = pytest.mark.django_db

# -------------------------------------------------
# Fixture Data
# -------------------------------------------------
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def unverify_client(api_client, user):
    refresh = RefreshToken.for_user(user)  
    access = str(refresh.access_token)  

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    return api_client


@pytest.fixture
def verify_client(api_client, user):
    user.email_verified = True
    user.save()
    
    api_client.force_authenticate(user=user)
    return api_client


# -------------------------------------------------
# User Login and Registration Test
# -------------------------------------------------
def test_customer_register(client):
    """Test New User Registrations and customer base role"""

    url = reverse("accounts:register")
    data = {
        "email":"customer@example.com",
        'role':"customer",
        'password':"Password123",
        'confirm_password':"Password123"
    }
    response = client.post(url,data,format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access' in response.data

def test_shop_owner_register(client):
    """Test New User Registrations and shop_owner base role"""

    url = reverse("accounts:register")
    data = {
        "email":"shop_owner@example.com",
        'role':"shop_owner",
        'password':"Password123",
        'confirm_password':"Password123"
    }
    response = client.post(url,data,format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access' in response.data

def test_user_login_and_send_auto_email_otp_for_unverify_user(unverify_client,user):
    """
    Test That after login will send otp
    Resonse: refresh, access, otp_message
    """

    url = reverse("accounts:login")
    assert user.email_otp is None
    assert user.email_otp_created_at is None

    response = unverify_client.post(url,{"email":user.email,"password":"TestPassword123"})
    assert response.status_code == status.HTTP_200_OK
    assert 'refresh' in response.data
    assert 'access' in response.data
    assert 'otp' in response.data

    user.refresh_from_db()

    assert user.email_otp is not None
    assert user.email_otp_created_at is not None


def test_user_login_and_send_auto_email_otp_for_verify_user(verify_client,user):
    """
    Test That after login will send otp
    Resonse: refresh, access
    """

    url = reverse("accounts:login")

    response = verify_client.post(url,{"email":user.email,"password":"TestPassword123"})
    assert response.status_code == status.HTTP_200_OK
    assert 'refresh' in response.data
    assert 'access' in response.data
    assert 'otp' not in response.data


def test_user_login_refresh(verify_client,user):
    """Test New User Registrations and customer base role"""

    url = reverse("accounts:login_refresh")
    refresh = RefreshToken.for_user(user)  
    access = str(refresh.access_token)  
    response = verify_client.post(url,{"refresh":str(refresh)})

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


def test_resend_otp(unverify_client,user):  
    """
    Test that for resend otp request
    """
    url = reverse("accounts:email_resend_otp")
    response = unverify_client.post(url,{"email":user.email})
    assert response.status_code == status.HTTP_200_OK


# -------------------------------------------------
# User Email Verify After Login
# -------------------------------------------------
def test_process_otp_verify_after_login(unverify_client,user): 
    """
    Test : After Login auto will send otp of his mail
    Then by confirm/otp api will send otp and email for verify this user email
    Response: 
    1. After Login will create email_otp and email_otp_created_at
    2. Then Send OTP and Email will email_verify=True and email_otp=None and email_otp_created_at = None
    """

    url = reverse("accounts:login")
    assert user.email_verified is False
    assert user.email_otp is None
    assert user.email_otp_created_at is None

    # Login and will send otp in mail
    response = unverify_client.post(url,{"email":user.email,"password":"TestPassword123"})
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'otp' in response.data

    user.refresh_from_db()

    # collect otp from user
    assert user.email_otp is not None
    verify_url = reverse("accounts:email_verify_otp")
    verify_data = {
        "email": user.email,
        "otp":user.email_otp 
    }
    verify_response = unverify_client.post(verify_url,verify_data)
    assert verify_response.status_code == status.HTTP_200_OK
    assert 'access' in verify_response.data
    assert 'refresh' in verify_response.data

    user.refresh_from_db()

    # After verify the email_verify will true and otp will none
    assert user.email_verified is True
    assert user.email_otp is None
    assert user.email_otp_created_at is None

 
# -------------------------------------------------
# User Email Verify With call Resend OTP
# -------------------------------------------------
def test_process_otp_verify_after_resend_otp(unverify_client,user): 
    """
    Test that login process with verify email
    """
    url = reverse("accounts:login")
    assert user.email_verified is False
    assert user.email_otp is None

    # Login and will send otp in mail
    response = unverify_client.post(url,{"email":user.email,"password":"TestPassword123"})
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'otp' in response.data

    user.refresh_from_db()

    # Resend Request for OTP
    assert user.email_otp is not None
    previous_otp = user.email_otp
    resend_otp_url = reverse("accounts:email_resend_otp")
    resend_otp_response = unverify_client.post(resend_otp_url,{"email":user.email})
    assert resend_otp_response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.email_otp != previous_otp

    verify_url = reverse("accounts:email_verify_otp")
    verify_data = {
        "email": user.email,
        "otp":user.email_otp 
    }
    verify_response = unverify_client.post(verify_url,verify_data)
    assert verify_response.status_code == status.HTTP_200_OK
    assert 'access' in verify_response.data
    assert 'refresh' in verify_response.data

    user.refresh_from_db()

    # After verify the email_verify will true and otp will none
    assert user.email_verified is True
    assert user.email_otp is None
    assert user.email_otp_created_at is None

def test_email_verify_by_wrong_email(unverify_client,user):
    """
    Test that verify email by wrong email request
    """
    url = reverse("accounts:login") 

    # Login and will send otp in mail
    response = unverify_client.post(url,{"email":user.email,"password":"TestPassword123"})
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'otp' in response.data

    user.refresh_from_db()

    # collect otp from user
    assert user.email_otp is not None
    verify_url = reverse("accounts:email_verify_otp")
    verify_data = { "email": 'wrong@example.com', "otp":user.email_otp } # Wrong email
    verify_response = unverify_client.post(verify_url,verify_data)

    assert verify_response.status_code == status.HTTP_400_BAD_REQUEST 
  
    assert user.email_verified is False 

def test_email_verify_by_wrong_otp(unverify_client,user):
    """
    Test that by use wrong otp
    """
    url = reverse("accounts:login") 

    # Login and will send otp in mail
    response = unverify_client.post(url,{"email":user.email,"password":"TestPassword123"})
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'otp' in response.data

    user.refresh_from_db()

    # collect otp from user
    assert user.email_otp is not None
    verify_url = reverse("accounts:email_verify_otp")
    verify_data = { "email": user.email,"otp": 123456} # Wrong otp
    verify_response = unverify_client.post(verify_url,verify_data)

    assert verify_response.status_code == status.HTTP_400_BAD_REQUEST 
  
    assert user.email_verified is False 


# -------------------------------------------------
# Test for verified user access Profile
# -------------------------------------------------
def test_get_profile(verify_client,user):
    """Test get Profile data for verifyed user """
    url = reverse("accounts:profile")
    response = verify_client.get(url) 
    assert response.status_code == status.HTTP_200_OK 


def test_patch_profile(verify_client,user):
    """Test Patch Update Profile data for verifyed user """
    url = reverse("accounts:profile") 

    response = verify_client.patch(url,{'email':"newemail@example.com"})
    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.email == 'newemail@example.com' 

def test_put_profile(verify_client,user):
    """Test PUT Update Profile data for verifyed user """

    url = reverse("accounts:profile")
    response = verify_client.put(url,{'email':'newemail@example.com','username':"newusername"})
    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.username == 'newusername'
    assert user.email == 'newemail@example.com'
    assert user.email_verified is False

def test_delete_profile(verify_client,user):
    """Test Delete Profile data for verifyed user, Response Delete method not allow"""

    url = reverse("accounts:profile")
    response = verify_client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

 

# -------------------------------------------------
# Test for Un verified user access Profile
# -------------------------------------------------
def test_get_profile_for_un_verify_user(unverify_client,user):
    "Test Get Profile for unverifyuser "
    url = reverse("accounts:profile")
    response = unverify_client.get(url)

    assert response.status_code == status.HTTP_200_OK 
    
def test_update_profile_for_un_verify_user(unverify_client,user):
    """Test that update block for un-verify user """

    url = reverse("accounts:profile")
    response = unverify_client.patch(url,{'role':"shop_owner"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = unverify_client.put(url,{'email':"update@example.com",'role':"shop_owner"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_profile_for_un_verify_user(unverify_client,user):
    """Test that delete profile data method not allow"""

    url = reverse("accounts:profile")
    response = unverify_client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_resend_otp_unauthenticated(client,user):  
    """Test resend otp not allow without header access key"""

    url = reverse("accounts:email_resend_otp")
    response = client.post(url,{"email":user.email})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED