# --------------------
# Message Message
# --------------------
MESSAGE_TYPE = [
    ('sms','SMS'),
    ('whatsapp','WhatsApp'),
    ('email','Email'),
    ('push','Push Notification'),
]
MESSAGE_STATUS = [
    ('draft','Active'),
    ('active','Active'),
    ('archived','Archived') 
]
# --------------------
# Message Campaign
# --------------------
SEND_TO_CHOICES = (
    ("all", "All Customers"),
    ("selected", "Selected Customers"),
    ("segment", "Customer Segment"),
)

# --------------------
# Message Log
# --------------------
MESSAGE_LOG_STATUS  = (
    ("pending", "Pending"),
    ("sent", "Sent"),
    ("delivered", "Delivered"),
    ("viewed", "Viewed"),
    ("failed", "Failed"),
)
