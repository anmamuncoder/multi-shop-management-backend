# Shop Management System

A modern Django-based shop management platform with async task processing, built for scalability and performance.

##  Features 

> **Product Management** – Product catalog, categories, variants, images, inventory, search, and filtering   <br>
> **Order Processing** – End-to-end order lifecycle including placement, tracking, cancellation, and fulfillment   <br>
> **User Accounts** – Secure authentication, role-based access, profile management, OTP, and email verification  <br>
> **Transactions & Payments** – Wallet top-ups, admin bank access, transaction history, and financial tracking  <br>
> **Real-time Chat** – Instant messaging with chat channels and real-time communication support  <br>
> **Messaging & Campaigns** – Email, SMS, WhatsApp, and notification templates with campaign and log management  <br>
> **Background Tasks** – Asynchronous processing using Celery for emails, notifications, and heavy jobs  <br>
> **Database** – Robust and scalable data storage powered by **PostgreSQL**  <br>
> **RESTful API** – OpenAPI-compliant, frontend-ready REST APIs with modular documentation   <br>

> **Security** – JWT authentication, role-based access control (RBAC), and permission enforcement  <br> 
> **Caching & Performance** – Redis-based caching for fast, scalable API performance  <br>
> **Validation & Error Handling** – Centralized request validation and consistent API error responses   <br>
> **Pagination & Filtering** – Optimized data retrieval for large datasets   <br>
> **Logging & Monitoring** – Structured logs and activity tracking for debugging and auditing   <br>

## Prerequisites 

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **Git** (latest stable version recommended)  
- **Daphne** (ASGI server for running the application)

<br>

## ⚡ Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/VTS-learn/team-setu-be.git
cd team-setu-be
```

### 2. Configure Environment

Create `.env` file in project root:

```env
# Server Configuration

COMPOSE_PROJECT_NAME=multi_shop_management

WEB_PORT=8020
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=django-insecure-kq^st_dx6s-%fn-x-xyjacw1t@rph0-bfv9i-op!w$=eci)sfw

# Database
POSTGRES_DB=multi_shop_management_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# EMAIL CONFIGURATION
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-email-address
EMAIL_HOST_PASSWORD=your-email-app-secure-password

# Redis & Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

#  MISC SETTINGS 
TIME_ZONE=Asia/Dhaka
LANGUAGE_CODE=en-us
```

### 3. Launch Application

```bash
# Build containers
docker compose -f docker-compose-dev.yml build

# Start services
docker compose -f docker-compose-dev.yml up -d

# Run migrations
docker compose -f docker-compose-dev.yml exec web python manage.py migrate

# Create admin user
docker compose -f docker-compose-dev.yml exec web python manage.py createsuperuser
```

### 4. Access Application

- **API/Web:** http://localhost:8020
- **Admin Panel:** http://localhost:8020/admin

<br>

---

<br>

### 5.  Location of API Docs OpenAPI 3.0 specification
 
#### **How to View the API Documentation**

You can load the file directly in Swagger Online Editor: <br>
🔗 **Swagger Online Editor** [editor.swagger.io](https://editor.swagger.io/)

**Steps:**

1. Open the Swagger Editor link above.
2. On the top menu, click **File → Import File → Paste JSON/YAML**.
3. Open the `docs/*.yml` file from this repository on GitHub.
4. Copy the entire contents of the YAML file.
5. Paste it into the Swagger Editor.
6. The interactive API documentation will load automatically.

<br>

```shell
docs/
├── authentication.yml       # Authentication APIs (9 endpoints)
│                             # Login, Register, OTP, Email Verification, Password Reset, Token Refresh, Profile Data etc.
│
├── shop_public.yml           # Public Shop APIs (10 endpoints)
│                             # public Shop listing & details, product category, product variant, product image, product view, search, filter, etc. 
│
├── shop_owner.yml            # Shop Owner APIs (29 endpoints)
│                             # Shop management, product CRUD, category CRUD, product variant CRUD, product images CRUD
│
├── order_customer.yml        # Customer Order APIs (12 endpoints)
│                             # Place order, order items,  order history, order details, cancel order, etc.
│
├── order_owner.yml           # Shop Owner Order APIs (5 endpoints)
│                             # View orders, update order status, order processing
│
├── transactions.yml          # Transaction APIs (6 endpoints)
│                             # View Admin Bank Account, Shop Owner TopUp, transaction history, 
│
├── template_messaging.yml    # Messaging Template APIs (18 endpoints)
│                             # CRUD Email/SMS/Notification/WhatsApp templates, campaign CRUD, Log preview, All Customer View
│
├── real_time_chat.yml        # Real-time Chat APIs (5 endpoints)
│                             # Chat Channel, Chat messages, real-time communication
```

 
## Quick Stats

| Category | Endpoint Count | Documentation |
|----------|---------------|---------------|
| Authentication | 9 | [`authentication.yml`](./authentication.yml) |
| Shop Public | 10 | [`shop_public.yml`](./shop_public.yml) |
| Shop Owner | 29 | [`shop_owner.yml`](./shop_owner.yml) |
| Order Customer | 12 | [`order_customer.yml`](./order_customer.yml) |
| Order Owner | 5 | [`order_owner.yml`](./order_owner.yml) |
| Transactions | 6 | [`transactions.yml`](./transactions.yml) |
| Template Messaging | 18 | [`template_messaging.yml`](./template_messaging.yml) |
| Real-Time Chat | 5 | [`real_time_chat.yml`](./real_time_chat.yml) |
| **Total** | **94** | - |



<br>

---

<br>


## 🖥 CMS App - Admin Dashboard

This app manages the **homepage content** of the website. It is **backend-only** and does **not provide APIs**. Content is managed via the Django admin and rendered in the frontend templates.

### Features

- **Wireframe** – Manage website branding and social media links.  
- **Testimonials** – Add and display user or customer feedback.  
- **FAQs** – Maintain frequently asked questions and answers for the homepage.  
- **Features** – Define homepage features with title, description, and pricing.

### Admin Access

- Navigate to `/admin` after logging in as a superuser or staff.  
- The dashboard provides access to the above sections:


> All content is handled through the Django admin interface. These models are used for rendering the homepage and other frontend sections.

<br>

---

<br>

## 📁 Project Structure

```
team-setu-be/
├── apps/
│   ├── base/           # Core functionality
│   ├── accounts/       # User management
│   ├── store/          # Product catalog
│   ├── order/          # Order processing
│   ├── chat/          # Customer vs Owner Chat
│   ├── transaction/          # Transaction system
│   ├── messaging/          # Template messaging
│   └── cms/          # content management system
├── core/
│   ├── settings.py     # Django configuration
│   └── asgi.py         # ASGI config
├── docs/ 
│   └── openapi.yml     # API Documentation
├── media/
│   └── All Media Files
├── templates/
│   └── All Templates
├── .env
├── .gitignore
├── docker-compose-dev.yml
├── Dockerfile.dev
├── Dockerfile.prod
├── requirements.txt 
├── pytest.ini
└── manage.py
```


## 🔧 Development

### Essential Commands

```bash
# Start development environment
docker compose -f docker-compose-dev.yml up

# View logs
docker compose -f docker-compose-dev.yml logs -f web

# Run migrations
docker compose -f docker-compose-dev.yml exec web python manage.py migrate

# Create migrations
docker compose -f docker-compose-dev.yml exec web python manage.py makemigrations

# Create super/staff/admin user
docker compose -f docker-compose-dev.yml exec web python manage.py createsuperuser

# Django shell
docker compose -f docker-compose-dev.yml exec web python manage.py shell

# Stop all services
docker compose -f docker-compose-dev.yml down
```

### Database Operations

```bash
# Backup
docker compose -f docker-compose-dev.yml exec db pg_dump -U postgres multi_shop_management > backup.sql

# Restore
cat backup.sql | docker compose -f docker-compose-dev.yml exec -T db psql -U postgres multi_shop_management

# Access database
docker compose -f docker-compose-dev.yml exec db psql -U postgres -d multi_shop_management
```



## Support

- 📧 Contact development team
- 🐛 [Report issues](https://github.com/anmamuncoder/)
- 📖 Check documentation

---

**Built with , using Django, PostgreSQL, Redis, and Celery**
 
> [`Author`](https://github.com/anmamuncoder)
> [`Project`](https://github.com/VTS-learn/team-setu-be.git)