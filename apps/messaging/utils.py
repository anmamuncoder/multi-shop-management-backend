from typing import List
from django.core.mail import EmailMultiAlternatives
from apps.messaging.models import TemplateMessage, MessageCampaign, MessageLog
from apps.accounts.models import User
from django.utils.html import escape 
import re 


# -----------------------------
# EMAIL
# -----------------------------
def send_bulk_email(campaign: MessageCampaign, users: List[User]):
    """
    Send bulk emails using TemplateMessage.body as raw HTML + CSS.
    - template: TemplateMessage instance (template.body contains full HTML & CSS)
    - users: list of User objects
    """
    if not users:
        return
    
    template = campaign.template
    from_email = "no-reply@yourdomain.com"

    # Fallback plain text (strip HTML tags)
    text_body = re.sub(r'<[^>]+>', '', template.body)
    messages = []

    for user in users:
        if not user.email:
            continue
        
        log = MessageLog.objects.filter(campaign=campaign, customer=user).first()
        # pixel_url = f"https://yourdomain.com/messaging/track_open/{log.id}/" 
        # html_body = template.body + f'<img src="{escape(pixel_url)}" width="1" height="1" style="display:none;" alt=""/>' 

        msg = EmailMultiAlternatives(
            subject=template.title,
            body=text_body,  
            from_email=from_email,
            to=[user.email]
        ) 
        msg.attach_alternative(template.body, "text/html")
        # msg.attach_alternative(html_body, "text/html")
        messages.append(msg)

    # Send all emails
    for msg in messages:
        msg.send(fail_silently=False)  

    return True
# -----------------------------
# PUSH
# -----------------------------
def send_push_notifications(template: TemplateMessage, users: List[User]):
    user_ids = [u.id for u in users]
    if not user_ids:
        return
    print(f"Sent PUSH '{template.title}' to {user_ids}")


# -----------------------------
# WHATSAPP
# -----------------------------
def send_whatsapp_messages(template: TemplateMessage, users: List[User]):
    phones = [u.phone for u in users if u.phone]
    if not phones:
        return
    print(f"Sent WHATSAPP '{template.title}' to {phones}")


# -----------------------------
# SMS
# -----------------------------
def send_sms_messages(template: TemplateMessage, users: List[User]):
    phones = [u.phone for u in users if u.phone]
    if not phones:
        return
    print(f"Sent SMS '{template.title}' to {phones}")
