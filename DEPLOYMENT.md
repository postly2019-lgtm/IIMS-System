# 🚀 دليل النشر الشامل - IIMS System Deployment Guide

## نظام إدارة المعلومات الاستخباراتية
## Intelligence Information Management System

---

## 📋 جدول المحتويات

1. [متطلبات النشر](#متطلبات-النشر)
2. [النشر على Railway](#النشر-على-railway)
3. [النشر على Render](#النشر-على-render)
4. [النشر على Vercel](#النشر-على-vercel)
5. [النشر باستخدام Docker](#النشر-باستخدام-docker)
6. [إعدادات قاعدة البيانات](#إعدادات-قاعدة-البيانات)
7. [متغيرات البيئة](#متغيرات-البيئة)
8. [الفحوصات الصحية](#الفحوصات-الصحية)
9. [استكشاف الأخطاء](#استكشاف-الأخطاء)

---

## متطلبات النشر

### المتطلبات الأساسية

- **Python**: 3.11.0 أو أحدث
- **Django**: 5.0.1
- **قاعدة البيانات**: PostgreSQL (موصى به للإنتاج) أو SQLite (للتطوير فقط)
- **خادم التطبيق**: Gunicorn
- **خادم الملفات الثابتة**: WhiteNoise

### المتطلبات الاختيارية

- **Groq API Key**: للميزات الذكية (الترجمة والتحليل)
- **Domain Name**: للنشر على نطاق مخصص
- **SSL Certificate**: يتم توفيره تلقائياً من معظم المنصات

---

## النشر على Railway

### ⚡ النشر السريع (Quick Deploy)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

### 📝 النشر اليدوي (Manual Deployment)

#### 1. إنشاء حساب Railway

1. انتقل إلى [railway.app](https://railway.app)
2. سجل الدخول باستخدام GitHub
3. أنشئ مشروع جديد (New Project)

#### 2. ربط المستودع

```bash
# في مجلد المشروع
git init
git add .
git commit -m "Initial commit for Railway deployment"
git remote add origin <your-github-repo-url>
git push -u origin main
```

#### 3. إعداد المشروع في Railway

1. اختر "Deploy from GitHub repo"
2. اختر مستودع IIMS-System
3. Railway سيكتشف تلقائياً أنه مشروع Django

#### 4. إضافة قاعدة بيانات PostgreSQL

1. في لوحة تحكم Railway، اضغط "+ New"
2. اختر "Database" → "PostgreSQL"
3. Railway سيوفر `DATABASE_URL` تلقائياً

#### 5. تكوين متغيرات البيئة

في قسم "Variables" في Railway، أضف:

```env
# Required
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app

# Database (provided automatically by Railway)
# DATABASE_URL=postgresql://...

# Admin User
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@iims.local
ADMIN_PASSWORD=your-secure-password-here
ADMIN_JOB_NUMBER=ADMIN-001

# Optional: Groq AI
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Optional: Custom Domain
# CSRF_TRUSTED_ORIGINS=https://your-domain.com
```

#### 6. توليد SECRET_KEY

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### 7. النشر

Railway سينشر تلقائياً عند:
- Push إلى GitHub
- تغيير متغيرات البيئة
- إعادة النشر يدوياً

#### 8. التحقق من النشر

```bash
# افتح التطبيق
https://your-app.railway.app

# تحقق من الصحة
https://your-app.railway.app/health/
```

### 🔧 إعدادات Railway المتقدمة

#### تخصيص عملية البناء

ملف `railway.json` موجود بالفعل:

```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "bash build.sh"
  },
  "deploy": {
    "startCommand": "bash startup.sh",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### تخصيص عدد Workers

```env
WEB_CONCURRENCY=3  # عدد Gunicorn workers
```

#### إعداد Domain مخصص

1. في Railway Dashboard → Settings → Domains
2. أضف نطاقك المخصص
3. أضف CNAME record في DNS provider:
   ```
   CNAME: your-domain.com → your-app.railway.app
   ```
4. حدّث متغيرات البيئة:
   ```env
   ALLOWED_HOSTS=your-domain.com,your-app.railway.app
   CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://your-app.railway.app
   ```

---

## النشر على Render

### 📝 خطوات النشر

#### 1. إنشاء حساب Render

1. انتقل إلى [render.com](https://render.com)
2. سجل الدخول باستخدام GitHub

#### 2. إنشاء Web Service

1. Dashboard → New → Web Service
2. اختر مستودع IIMS-System
3. املأ التفاصيل:
   - **Name**: iims-system
   - **Environment**: Python 3
   - **Build Command**: `bash build.sh`
   - **Start Command**: `bash startup.sh`

#### 3. إضافة قاعدة بيانات

1. Dashboard → New → PostgreSQL
2. انسخ Internal Database URL
3. أضفه كمتغير بيئة `DATABASE_URL`

#### 4. تكوين متغيرات البيئة

```env
SECRET_KEY=your-generated-secret-key
DEBUG=False
PYTHON_VERSION=3.11.0
ADMIN_PASSWORD=your-secure-password
GROQ_API_KEY=your-groq-key (optional)
```

#### 5. النشر

Render سينشر تلقائياً عند Push إلى GitHub.

---

## النشر على Vercel

### ⚠️ ملاحظة مهمة

Vercel مناسب للتطبيقات Serverless، لكن Django يعمل بشكل أفضل على Railway أو Render.

### 📝 خطوات النشر (إذا كنت تفضل Vercel)

#### 1. تثبيت Vercel CLI

```bash
npm install -g vercel
```

#### 2. تسجيل الدخول

```bash
vercel login
```

#### 3. تكوين المشروع

ملف `vercel.json` موجود بالفعل، لكن يجب تحديثه:

```json
{
  "builds": [
    {
      "src": "config/wsgi.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.11"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "config/wsgi.py"
    }
  ]
}
```

#### 4. إضافة متغيرات البيئة

```bash
vercel env add SECRET_KEY
vercel env add DATABASE_URL
vercel env add ADMIN_PASSWORD
```

#### 5. النشر

```bash
vercel --prod
```

---

## النشر باستخدام Docker

### 📦 استخدام Dockerfile الموجود

#### 1. بناء الصورة

```bash
docker build -t iims-system:latest .
```

#### 2. تشغيل الحاوية

```bash
docker run -d \
  --name iims-system \
  -p 8004:8004 \
  -e SECRET_KEY="your-secret-key" \
  -e DEBUG=False \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e ADMIN_PASSWORD="your-password" \
  iims-system:latest
```

#### 3. استخدام Docker Compose

إنشاء `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8004:8004"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/iims
      - ADMIN_PASSWORD=${ADMIN_PASSWORD}
    depends_on:
      - db
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=iims
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

تشغيل:

```bash
docker-compose up -d
```

---

## إعدادات قاعدة البيانات

### PostgreSQL (موصى به للإنتاج)

#### Railway

Railway يوفر PostgreSQL تلقائياً. فقط أضف Database من Dashboard.

#### Render

```bash
# Render يوفر Internal Database URL
DATABASE_URL=postgresql://user:pass@host/database
```

#### يدوياً

```bash
# إنشاء قاعدة بيانات
createdb iims_production

# تكوين DATABASE_URL
export DATABASE_URL="postgresql://user:password@localhost:5432/iims_production"

# تشغيل Migrations
python manage.py migrate
```

### SQLite (للتطوير فقط)

```env
# لا حاجة لـ DATABASE_URL
# Django سيستخدم db.sqlite3 تلقائياً
```

---

## متغيرات البيئة

### المتغيرات الإلزامية

| المتغير | الوصف | مثال |
|---------|--------|------|
| `SECRET_KEY` | مفتاح Django السري | `django-insecure-xxx...` |
| `DEBUG` | وضع التطوير | `False` |
| `ALLOWED_HOSTS` | النطاقات المسموحة | `app.railway.app` |

### المتغيرات الموصى بها

| المتغير | الوصف | مثال |
|---------|--------|------|
| `DATABASE_URL` | رابط قاعدة البيانات | `postgresql://...` |
| `ADMIN_PASSWORD` | كلمة مرور المدير | `SecurePass123!` |
| `GROQ_API_KEY` | مفتاح Groq AI | `gsk_xxx...` |

### المتغيرات الاختيارية

| المتغير | الوصف | القيمة الافتراضية |
|---------|--------|-------------------|
| `WEB_CONCURRENCY` | عدد Workers | `3` |
| `PORT` | منفذ التطبيق | `8004` |
| `GROQ_MODEL` | نموذج Groq | `llama-3.3-70b-versatile` |

راجع `.env.production.example` للقائمة الكاملة.

---

## الفحوصات الصحية

### Endpoints المتاحة

#### 1. Basic Health Check
```bash
GET /health/
```

**Response:**
```json
{
  "status": "healthy",
  "checks": {
    "database": {
      "status": "healthy",
      "message": "Database connection successful"
    }
  }
}
```

#### 2. Detailed Health Check (Staff Only)
```bash
GET /health/detailed/
```

#### 3. Readiness Probe
```bash
GET /health/ready/
```

#### 4. Liveness Probe
```bash
GET /health/live/
```

### استخدام سكريبت الفحص

```bash
# تشغيل الفحص الشامل
python health_check.py

# سيعرض:
# ✅ Database Connection
# ✅ Migrations
# ✅ Static Files
# ⚠️  Environment Variables
# etc.
```

---

## استكشاف الأخطاء

### مشكلة: Application Error 503

**الحل:**
1. تحقق من logs:
   ```bash
   # Railway
   railway logs
   
   # Render
   # انظر Logs في Dashboard
   ```

2. تحقق من DATABASE_URL
3. تحقق من Migrations:
   ```bash
   python manage.py showmigrations
   ```

### مشكلة: Static Files لا تظهر

**الحل:**
```bash
# أعد جمع الملفات الثابتة
python manage.py collectstatic --clear --noinput

# تحقق من STATIC_ROOT
echo $STATIC_ROOT
```

### مشكلة: CSRF Verification Failed

**الحل:**
```env
# أضف نطاقك إلى CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://your-app.railway.app
```

### مشكلة: Database Connection Failed

**الحل:**
1. تحقق من DATABASE_URL
2. تحقق من أن PostgreSQL يعمل
3. تحقق من الاتصال:
   ```bash
   python manage.py dbshell
   ```

### مشكلة: Groq AI لا يعمل

**الحل:**
```bash
# تحقق من المفتاح
echo $GROQ_API_KEY

# تحقق من التثبيت
pip list | grep groq

# اختبر الاتصال
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

---

## 📞 الدعم والمساعدة

### الموارد

- **Documentation**: [README.md](README.md)
- **Environment Variables**: [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)
- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/5.0/howto/deployment/

### الإبلاغ عن المشاكل

إذا واجهت مشكلة:
1. تحقق من Logs
2. راجع قسم استكشاف الأخطاء
3. أنشئ Issue على GitHub

---

## ✅ قائمة فحص ما قبل النشر

- [ ] تم توليد SECRET_KEY قوي
- [ ] DEBUG=False
- [ ] تم تكوين ALLOWED_HOSTS
- [ ] تم تكوين CSRF_TRUSTED_ORIGINS
- [ ] تم إعداد PostgreSQL
- [ ] تم تشغيل Migrations
- [ ] تم جمع Static Files
- [ ] تم تكوين ADMIN_PASSWORD
- [ ] تم اختبار /health/ endpoint
- [ ] تم اختبار تسجيل الدخول
- [ ] تم مراجعة إعدادات الأمان

---

**🎉 مبروك! نظام IIMS جاهز للنشر!**

للمزيد من المعلومات، راجع [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)
