from rest_framework_simplejwt.tokens import RefreshToken  
from django.utils.text import slugify
import uuid

def make_token_key(user, access_keys):
        """
        Generate token key and in access key include some user data
        Args:
            user(Model Object) : User object
            access_key : list of include data in access token
        Returns:
            list [] of access token and refresh token
        """
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        for field in access_keys:
            if hasattr(user, field):
                value = getattr(user, field)
                # Convert UUIDs and other non-JSON-serializable types to string
                if isinstance(value, (uuid.UUID,)):
                    value = str(value)
                access_token[field] = value
        return access_token , refresh_token


def generate_unique_slug(model_class, name, slug_field='slug'):
    """
    Generate a unique slug for any Django model.
    Args:
        model_class (Model Class): The Django model class for which the slug is generated.
        name (str): The value (usually a name field) to create the slug from.
        slug_field (str, optional): The name of the slug field in the model. Defaults to 'slug'.

    Returns:
        str: A unique slug string that does not exist in the model's table.
    """

    base_slug = slugify(name)
    slug = base_slug
    n = 1

    # Avoid duplicate slugs
    while model_class.objects.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{n}"
        n += 1
    return slug
