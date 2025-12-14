from celery import shared_task
from django.core.mail import EmailMessage
from django.utils import timezone
from .models import User
import random


@shared_task
def task_send_email_otp(user_id):
    """Task for Send 6 Digit OTP in Email at the User"""

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValueError("User not valid")

    otp = random.randint(100000, 999999)
    
    user.email_otp = otp
    user.email_otp_created_at = timezone.now()
    user.save(update_fields=['email_otp', 'email_otp_created_at']) 

    # -------------------------------
    # Send OTP Email
    # -------------------------------  
    subject = "Your OTP Verification Code"
    body = f"Dear {user.email},\n\nYour OTP code is: {otp}\nThis code is valid for 5 minutes.\n\nThank you."
    email = EmailMessage(
        subject=subject,
        body=body,
        to=[user.email],
    )
    email.send(fail_silently=False)

    return "OTP sent successfully"
