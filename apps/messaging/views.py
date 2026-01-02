from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone 

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from apps.base.permissions import IsShopOwner
from apps.base.paginations import BasePagination
from apps.accounts.models import User

from .models import TemplateMessage, MessageCampaign, MessageLog
from .serializers import TemplateMessageSerializer, MessageCampaignSerializer, MessageLogSerializer,CustomerSerializer
from .services.campaign_service import MessageCampaignService
 

# --------------------------------
# GET - shop_owner
# --------------------------------
class TemplateMessageView(ModelViewSet):
    serializer_class = TemplateMessageSerializer
    permission_classes = [IsAuthenticated,IsShopOwner]
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["channel_to", "status", "is_active"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'shop'):
            return TemplateMessage.objects.filter(shop=user.shop)
        return TemplateMessage.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not user or not user.is_authenticated or not hasattr(user, 'shop'):
            raise PermissionDenied("You must be a verified shop owner to create templates.")
        serializer.save(shop=user.shop)

    def perform_update(self, serializer):
        user = self.request.user
        instance = serializer.instance
        if not user or not user.is_authenticated or not hasattr(user, 'shop') or instance.shop != user.shop:
            raise PermissionDenied("You do not have permission to update this template.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if not user or not user.is_authenticated or not hasattr(user, 'shop') or instance.shop != user.shop:
            raise PermissionDenied("You do not have permission to delete this template.")
        instance.delete()

# --------------------------------
# GET - shop_owner
# --------------------------------
class MessageCampaignView(ModelViewSet):
    serializer_class = MessageCampaignSerializer
    permission_classes = [IsAuthenticated, IsShopOwner]
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["send_to", "scheduled_at", "is_sent"]

    def get_queryset(self): 
        user = self.request.user
        if hasattr(user, "shop"):
            return MessageCampaign.objects.filter(shop=user.shop)
        return MessageCampaign.objects.none()

    # -------------------------
    # Helper function for validation
    # -------------------------
    def _validate_user_shop_access(self, campaign=None, check_sent=False):
        user = self.request.user
        if not hasattr(user, "shop"):
            raise PermissionDenied("You must have a shop.")
        if campaign and campaign.shop != user.shop:
            raise PermissionDenied("You do not have permission for this campaign.")
        if check_sent and campaign and campaign.is_sent:
            raise PermissionDenied("Cannot modify a campaign that is already sent.")

    # -------------------------
    # CRUD Overrides
    # -------------------------
    def perform_create(self, serializer): 
        self._validate_user_shop_access()
        serializer.save(shop=self.request.user.shop)

    def perform_update(self, serializer): 
        raise PermissionDenied("Campaigns cannot be updated once created.")

    def perform_destroy(self, instance): 
        self._validate_user_shop_access(instance, check_sent=True)

        # Block if campaign is already sent
        if instance.is_sent:
            raise PermissionDenied("Cannot delete a campaign that is already sent.")
        
        instance.delete()

    # -------------------------
    # Custom Actions
    # -------------------------
    @action(detail=True, methods=["post"])
    def mark_sent(self, request, pk=None):
        """Mark a campaign as sent and trigger charging logic."""
        campaign = self.get_object()

        # Validate access and that campaign is not already sent
        self._validate_user_shop_access(campaign, check_sent=True)

        # Trigger charging service
        success, result = MessageCampaignService.process_campaign(campaign)

        if success:
            # Mark as sent
            campaign.is_sent = True
            campaign.save(update_fields=["is_sent","updated_at"])

        return Response({"status": "marked_sent",**result}, status=status.HTTP_200_OK)
    

# --------------------------------
# GET - shop_owner,customer
# --------------------------------
class MessageLogView(ReadOnlyModelViewSet):
    serializer_class = MessageLogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "campaign", "customer"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'shop_owner' and hasattr(user, 'shop'):
            # Shop owner sees logs for their shop's campaigns
            return MessageLog.objects.filter(campaign__shop=user.shop).order_by('-created_at')
        if user.is_authenticated:
            # Customers see their own logs
            return MessageLog.objects.filter(customer=user).order_by('-created_at')
        return MessageLog.objects.none()


# --------------------------------
# Customer View 
# --------------------------------
class CustomerView(ReadOnlyModelViewSet):
    serializer_class = CustomerSerializer 
    permission_classes = [IsShopOwner]
    
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']
    search_fields = ['id','email']

    def get_queryset(self):
        return User.objects.filter(role='customer')


# --------------------------------
# Track_email_open
# --------------------------------
# def track_email_open(request, log_id):
#     """
#     When the email is opened and the pixel is requested,
#     update MessageLog as viewed.
#     """
#     log = get_object_or_404(MessageLog, id=log_id)

#     # Update only if not already viewed
#     if not log.viewed_at:
#         log.viewed_at = timezone.now()
#         log.status = 'viewed'
#         log.save(update_fields=['viewed_at', 'status','updated_at'])

#     # Return a 1x1 transparent GIF
#     pixel_gif = (
#         b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
#         b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
#         b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
#     )
#     return HttpResponse(pixel_gif, content_type="image/gif")
