# Shop Management System

A modern Django-based shop management platform with async task processing, built for scalability and performance.

##  Features

> **Product Management** - Comprehensive inventory and catalog system <br>
>  **Order Processing** - Complete order lifecycle management <br>
>  **User Accounts** - Customer and staff account management <br>
>  **Background Tasks** - Asynchronous processing with Celery <br>
>  **Caching** - Redis-powered performance optimization <br>
>  **RESTful API** - Modern API architecture for frontend integration <br>

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Git

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

COMPOSE_PROJECT_NAME=shop_management

WEB_PORT=8020
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=your-secret-key-here

# Database
POSTGRES_DB=shop_management
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
<br>

 

## 📁 Project Structure

```
team-setu-be/
├── apps/
│   ├── base/           # Core functionality
│   ├── accounts/       # User management
│   ├── store/          # Product catalog
│   └── order/          # Order processing
├── core/
│   ├── settings.py     # Django configuration
│   └── asgi.py         # ASGI config
├── docker-compose-dev.yml
├── Dockerfile
├── requirements.txt
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

# Django shell
docker compose -f docker-compose-dev.yml exec web python manage.py shell

# Stop all services
docker compose -f docker-compose-dev.yml down
```

### Database Operations

```bash
# Backup
docker compose -f docker-compose-dev.yml exec db pg_dump -U postgres shop_management > backup.sql

# Restore
cat backup.sql | docker compose -f docker-compose-dev.yml exec -T db psql -U postgres shop_management

# Access database
docker compose -f docker-compose-dev.yml exec db psql -U postgres -d shop_management
```



## Support

- 📧 Contact development team
- 🐛 [Report issues](https://github.com/anmamuncoder/)
- 📖 Check documentation

---

**Built with , using Django, PostgreSQL, Redis, and Celery**
 
> [`Author`](https://github.com/anmamuncoder)
> [`Project`](https://github.com/VTS-learn/team-setu-be.git)