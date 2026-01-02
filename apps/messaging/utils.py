from typing import List
from django.core.mail import EmailMultiAlternatives
from apps.messaging.models import TemplateMessage
from apps.accounts.models import User
import re

# -----------------------------
# EMAIL
# -----------------------------
def send_bulk_email(template: TemplateMessage, users: List[User]):
    """
    Send bulk emails using TemplateMessage.body as raw HTML + CSS.
    - template: TemplateMessage instance (template.body contains full HTML & CSS)
    - users: list of User objects
    """
    if not users:
        return

    from_email = "no-reply@yourdomain.com"

    # Fallback plain text (strip HTML tags)
    text_body = re.sub(r'<[^>]+>', '', template.body)

    messages = []
    for user in users:
        if not user.email:
            continue
        msg = EmailMultiAlternatives(
            subject=template.title,
            body=text_body,  
            from_email=from_email,
            to=[user.email]
        ) 
        msg.attach_alternative(template.body, "text/html")
        messages.append(msg)

    # Send all emails
    for msg in messages:
        msg.send(fail_silently=False)

    print(f"Sent HTML EMAIL to {len(messages)} users.")


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
