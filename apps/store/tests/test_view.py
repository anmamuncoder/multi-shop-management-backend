import pytest
from rest_framework.test import APIClient 
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.db import IntegrityError
# Internal
from .factories import ShopFactory,CategoryFactory,ProductFactory,ProductImageFactory,ProductVariantFactory
from apps.store.models import Shop,Category,Product,ProductImage,ProductVariant
# Enternal
from apps.accounts.models import User
from apps.accounts.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

# -----------------------------
# Factory
# -----------------------------

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def users():
    customer = UserFactory()
    owner = UserFactory()
    return owner, customer

@pytest.fixture
def client_user(client,users):
    """
    [authenticated shop owner, authenticated customer, unauthenticated public user]
    """ 
    owner, customer = users

 # separate clients
    owner_client = APIClient()
    customer_client = APIClient()
    public = APIClient()

    # owner token
    refresh_owner = RefreshToken.for_user(owner)
    access_owner = str(refresh_owner.access_token)
    owner_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_owner}")

    # customer token
    refresh_customer = RefreshToken.for_user(customer)
    access_customer = str(refresh_customer.access_token)
    customer_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_customer}")

    return owner_client, customer_client, public


@pytest.fixture
def shop(users):
    """
    Created : Shop and 1 Category and  6 Products
    """
    owner, customer = users
    shop = ShopFactory(owner=owner)
    shop.is_verified = True
    shop.save()

    cat1 = CategoryFactory(shop=shop)
    for i in range(0,5):
        product = ProductFactory(shop=shop,category=cat1)
    
    cat2 = CategoryFactory(shop=shop)
    product = ProductFactory(shop=shop,category=cat2)

    return shop


# -----------------------------
# Shop View Test
# -----------------------------
def test_shop_view(client_user):
    """
    Shop View allow for all user
    All User : Allow
    """

    url = reverse("store:shops-list")
    owner_client, customer_client, public = client_user

    response_owner = owner_client.get(url)
    response_customer = customer_client.get(url)
    response_public = public.get(url)

    assert response_owner.status_code == status.HTTP_200_OK
    assert response_customer.status_code == status.HTTP_200_OK
    assert response_public.status_code == status.HTTP_200_OK

def test_shop_retrive_by_slug_Owner(shop, client_user):
    """
    Test That by retrive data by slug field 
    All User : Allow
    """

    url = reverse("store:shops-detail", args=[shop.slug])
    owner_client, customer_client, public = client_user

    response_owner = owner_client.get(url) 

    assert response_owner.status_code == status.HTTP_200_OK 

def test_shop_retrive_by_slug_Customer(shop, client_user):
    """
    Test That by retrive data by slug field 
    All User : Allow
    """

    url = reverse("store:shops-detail", args=[shop.slug])
    owner_client, customer_client, public = client_user
 
    response_customer = customer_client.get(url) 
 
    assert response_customer.status_code == status.HTTP_200_OK 

def test_shop_retrive_by_slug_Public(shop, client_user):
    """
    Test That by retrive data by slug field 
    All User : Allow
    """

    url = reverse("store:shops-detail", args=[shop.slug])
    owner_client, customer_client, public = client_user
 
    response_public = public.get(url) 
    assert response_public.status_code == status.HTTP_200_OK 



def test_shop_retrive_limited_data_show_for_public(shop, client_user):
    """
    Shop View allow for all user
    Owner : Allow All Fields Data
    Customer/Public : Restricted data ('owner','is_verified','total_sales','is_active')
    """

    url = reverse("store:shops-detail", args=[shop.slug])
    owner_client, customer_client, public = client_user

    response_owner = owner_client.get(url)
    response_customer = customer_client.get(url)
    response_public = public.get(url)

    assert 'total_sales' in response_owner.data 
    assert 'owner' in response_owner.data 

    assert 'total_sales' not in response_customer 
    assert 'owner' not in response_customer 
    assert 'total_sales' not in response_public 

def test_shop_create_owner(client_user):
    """
    Test to try to create shop a ShopOwner User
    Return : OK
    """

    url = reverse("store:shops-list")   
    owner_client, customer_client, public = client_user  
    data = {
        'name':"test_create_shop",
        'description':"description",
        'short_intro':"short_intro",
        'policies':"policies",
        'currency':"BDT",
        'primary_color':"#000",
        'tax_rate':50.0
    } 
    response_owner = owner_client.post(url,data=data) 
    assert response_owner.status_code == status.HTTP_201_CREATED  

def test_shop_create_customer(client_user,users):
    """
    Test to try to create shop a ShopOwner User
    Return : 403 FORBIDDEN
    """

    url = reverse("store:shops-list")   
    owner, customer = users
    owner_client, customer_client, public = client_user  
    data = {
        'name':"test_create_shop",
        'description':"description",
        'short_intro':"short_intro",
        'policies':"policies",
        'currency':"BDT",
        'primary_color':"#000",
        'tax_rate':50.0
    } 
    assert customer.role is 'customer'
    response_customer = customer_client.post(url,data=data) 
    assert response_customer.status_code == status.HTTP_403_FORBIDDEN

def test_shop_create_public(client_user):
    """
    Test to try to create shop a ShopOwner User
    Return : 401 UNAUTHORIZED
    """

    url = reverse("store:shops-list")   
    owner_client, customer_client, public = client_user  
    data = {
        'name':"test_create_shop",
        'description':"description",
        'short_intro':"short_intro",
        'policies':"policies",
        'currency':"BDT",
        'primary_color':"#000",
        'tax_rate':50.0
    } 
    response_public = public.post(url,data=data) 
    assert response_public.status_code == status.HTTP_401_UNAUTHORIZED


def test_shop_create_twice_shop(users):
    """
    Only One shop allow to create shop owner
    """
    owner, customer = users

    # First shop creation 
    shop1 = ShopFactory(owner=owner)
    assert Shop.objects.filter(owner=owner).count() == 1

    # Second shop 
    with pytest.raises(IntegrityError):
        shop2 = ShopFactory(owner=owner)  
  
def test_shop_update_data_before_varify(users,client_user):
    """
    Test Update data before shop verifyed 
    Return: Forbidden
    """

    owner, customer = users
    shop = ShopFactory(owner=owner)

    url = reverse("store:shops-detail", args=[shop.slug])
    owner_client, customer_client, public = client_user  

    data = {'primary_color':"#000"} 
    response_owner = owner_client.patch(url,data=data) 

    assert response_owner.status_code == status.HTTP_403_FORBIDDEN


def test_shop_update_data_after_varify(users,client_user):
    """
    Test can able to update data after verify
    Return : Ok
    """
    
    owner, customer = users
    shop = ShopFactory(owner=owner)
    shop.is_verified = True
    shop.save()
    
    url = reverse("store:shops-detail", args=[shop.slug])
    owner_client, customer_client, public = client_user  

    data = {'primary_color':"#000"} 
    assert shop.primary_color != "#000"
    response_owner = owner_client.patch(url,data=data) 

    assert response_owner.status_code == status.HTTP_200_OK
    assert response_owner.data['primary_color'] == "#000"

def test_shop_delete_before_verify(users,client_user):
    """
    Test can delete to able before verify
    Return : OK
    """
    
    owner, customer = users
    owner_client, customer_client, public = client_user  

    shop = ShopFactory(owner=owner)
    assert Shop.objects.filter(owner=owner).count() == 1

    url = reverse("store:shops-detail", args=[shop.slug])
    response_owner = owner_client.delete(url) 
    assert response_owner.status_code == status.HTTP_204_NO_CONTENT

def test_shop_delete_after_verify(users,client_user):
    """
    Test can able to delete after verify
    Return : OK
    """
    
    owner, customer = users
    owner_client, customer_client, public = client_user  

    shop = ShopFactory(owner=owner)
    shop.is_verified = True
    shop.save()
    
    assert Shop.objects.filter(owner=owner).count() == 1
    assert shop.is_verified is True

    url = reverse("store:shops-detail", args=[shop.slug])
    response_owner = owner_client.delete(url) 
    assert response_owner.status_code == status.HTTP_204_NO_CONTENT
 



# -----------------------------
# Category View Test
# -----------------------------
def test_category_view_shop_owner(client_user):
    """
    Test able to view shop owner with secrete data
    Return : Okey
    """
    
    owner_client, customer_client, public = client_user
    url = reverse("store:categories-list")    
    
    response  = owner_client.get(url) 
    assert response.status_code == status.HTTP_200_OK

def test_category_view_shop_customer(client_user):
    """
    Test able to view shop Customer with limited data
    Return : Okey
    """
    
    owner_client, customer_client, public = client_user
    url = reverse("store:categories-list")    
    response  = customer_client.get(url) 
    assert response.status_code == status.HTTP_200_OK
 
def test_category_view_shop_public(client_user):
    """
    Test able to view public user with limited data
    Return : OK
    """
    
    owner_client, customer_client, public = client_user
    url = reverse("store:categories-list")    
    response  = public.get(url) 
    assert response.status_code == status.HTTP_200_OK

def test_category_create_shop_owner(client_user,users):
    """
    Test category create process the shop owner if has a shop
    Return : OK
    """
    
    owner, customer = users
    shop = ShopFactory(owner=owner)
    
    owner_client, customer_client, public = client_user
    url = reverse("store:categories-list")    
    data = { 'name':"test_create_customer",  } 
    response_owner = owner_client.post(url,data=data) 
    assert response_owner.status_code == status.HTTP_201_CREATED  

def test_category_create_customer(client_user):
    """
    Test Customer cant create category
    Return : Forbidden
    """
    
    owner_client, customer_client, public = client_user
    url = reverse("store:shops-list")     

    data = { 'name':"test_create_customer",}  
    response_customer = customer_client.post(url,data=data) 
    assert response_customer.status_code == status.HTTP_403_FORBIDDEN

def test_category_create_public(client_user):
    """
    Test Category Cant create public user 
    Return : Unauthorized    
    """

    owner_client, customer_client, public = client_user
    url = reverse("store:shops-list")     

    data = {'name':"test_create_public" } 
    response_public = public.post(url,data=data) 
    assert response_public.status_code == status.HTTP_401_UNAUTHORIZED

def test_category_update_shop_owner(client_user,users):
    """
    Test category update can able the shop owner 
    Return : No Content 204
    """
    
    owner_client, customer_client, public = client_user
    owner, customer = users
    shop = ShopFactory(owner=owner)
    
    owner_client, customer_client, public = client_user
    url = reverse("store:categories-list")    
    data = { 'name':"test_create_customer",  } 
    response_owner = owner_client.post(url,data=data) 
    assert response_owner.status_code == status.HTTP_201_CREATED  

    cat = Category.objects.filter(shop=shop).first() 
    url_delete = reverse("store:categories-detail", args=[cat.slug])
    response_owner = owner_client.delete(url_delete) 
    assert response_owner.status_code == status.HTTP_204_NO_CONTENT
 

# -----------------------------
# Product View Test
# -----------------------------
def test_product_view_owner(client_user):
    """
    Test That All Product can viewe Owenr with secute data
    Return : OK
    """
    
    owner_client, customer_client, public = client_user
    url = reverse("store:products-list")    
    response  = owner_client.get(url) 
    assert response.status_code == status.HTTP_200_OK 

def test_product_view_customer(client_user):
    """
    Test all product can view the customer with limited data
    Return : OK
    """
    
    owner_client, customer_client, public = client_user
    url = reverse("store:products-list")    
    response  = customer_client.get(url) 
    assert response.status_code == status.HTTP_200_OK 

def test_product_view_public(client_user):
    """
    Test all product can view the public with limited data
    Return : OK
    """
    owner_client, customer_client, public = client_user
    url = reverse("store:products-list")    
    response  = public.get(url) 
    assert response.status_code == status.HTTP_200_OK


def test_product_create_owner(client_user,users):
    """
    Test Owner can able to create new product if has a shop
    Return : OK
    """
    
    owner, customer = users
    shop = ShopFactory(owner=owner)
    cat = CategoryFactory(shop=shop)

    owner_client, customer_client, public = client_user
    url = reverse("store:products-list")    
    data = {
        'name':"test_product_create_owner",
        'category':cat.slug,
        'name':"short_intro",
        'short_description':"short_description",
        'full_description':"full_description", 
        'sku':"SKU123", 
    } 

    response = owner_client.post(url,data=data)
    assert response.status_code == status.HTTP_201_CREATED

def test_product_create_customer(client_user,users):
    """
    Test Customer cant able to request to create product
    Return: Forbidden
    """
    
    owner, customer = users
    shop = ShopFactory(owner=owner)
    cat = CategoryFactory(shop=shop) 
    owner_client, customer_client, public = client_user
    url = reverse("store:products-list")    
    data = {
        'name':"test_product_create_owner",
        'category':cat.slug,
        'name':"short_intro",
        'short_description':"short_description",
        'full_description':"full_description", 
        'sku':"SKU123", 
    }  
    response = customer_client.post(url,data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_product_create_public(client_user,users):
    """
    Test that cant reqeust public to create product
    Return : Unauthorized
    """
    
    owner, customer = users
    shop = ShopFactory(owner=owner)
    cat = CategoryFactory(shop=shop)

    owner_client, customer_client, public = client_user
    url = reverse("store:products-list")    
    data = {
        'name':"test_product_create_owner",
        'category':cat.slug,
        'name':"short_intro",
        'short_description':"short_description",
        'full_description':"full_description", 
        'sku':"SKU123", 
    } 

    response = public.post(url,data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
 
# -----------------------------
# Product Image View Test
# -----------------------------


# -----------------------------
# Product Variant View Test
# -----------------------------

