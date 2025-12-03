from rest_framework_simplejwt.tokens import RefreshToken  
import uuid

def make_token_key(user, access_keys):
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
