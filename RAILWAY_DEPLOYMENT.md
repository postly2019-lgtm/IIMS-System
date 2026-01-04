# 🚂 دليل النشر على Railway - Railway Deployment Guide

## نظام إدارة المعلومات الاستخباراتية - IIMS System

دليل شامل خطوة بخطوة للنشر على منصة Railway.

---

## 📋 جدول المحتويات

1. [لماذا Railway؟](#لماذا-railway)
2. [المتطلبات الأساسية](#المتطلبات-الأساسية)
3. [النشر السريع](#النشر-السريع)
4. [النشر اليدوي المفصل](#النشر-اليدوي-المفصل)
5. [إعداد قاعدة البيانات](#إعداد-قاعدة-البيانات)
6. [تكوين المتغيرات](#تكوين-المتغيرات)
7. [النطاقات المخصصة](#النطاقات-المخصصة)
8. [المراقبة والصيانة](#المراقبة-والصيانة)
9. [استكشاف الأخطاء](#استكشاف-الأخطاء)

---

## لماذا Railway؟

### ✅ المميزات

- **سهولة الاستخدام**: واجهة بسيطة وسهلة
- **نشر تلقائي**: من GitHub مباشرة
- **PostgreSQL مجاني**: قاعدة بيانات مدمجة
- **SSL مجاني**: شهادات SSL تلقائية
- **Logs مباشرة**: مراقبة فورية
- **دعم Docker**: مرونة كاملة
- **أسعار معقولة**: خطة مجانية سخية

### 💰 التسعير

- **Developer Plan**: $5/شهر
  - $5 رصيد شهري
  - مناسب للمشاريع الصغيرة
  
- **Hobby Plan**: $20/شهر
  - $20 رصيد شهري
  - مناسب للإنتاج

**ملاحظة:** IIMS System يستهلك تقريباً $3-5/شهر في الاستخدام المتوسط.

---

## المتطلبات الأساسية

### ✅ قبل البدء

- [ ] حساب GitHub
- [ ] مستودع IIMS-System على GitHub
- [ ] حساب Railway ([railway.app](https://railway.app))
- [ ] مفتاح Groq API (اختياري)

---

## النشر السريع

### ⚡ نشر بنقرة واحدة

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR_USERNAME/IIMS-System)

**الخطوات:**
1. اضغط على الزر أعلاه
2. سجل الدخول إلى Railway
3. اختر المستودع
4. املأ المتغيرات المطلوبة
5. اضغط "Deploy"

**⏱️ الوقت المتوقع:** 5-10 دقائق

---

## النشر اليدوي المفصل

### 📝 الخطوة 1: إنشاء حساب Railway

1. انتقل إلى [railway.app](https://railway.app)
2. اضغط "Login"
3. اختر "Login with GitHub"
4. امنح الصلاحيات المطلوبة

---

### 📝 الخطوة 2: إنشاء مشروع جديد

1. من Dashboard، اضغط "New Project"
2. اختر "Deploy from GitHub repo"
3. اختر مستودع `IIMS-System`
4. Railway سيبدأ بالكشف التلقائي

**ما يحدث الآن:**
- Railway يكتشف أنه مشروع Python/Django
- يقرأ `requirements.txt`
- يقرأ `railway.json` للإعدادات
- يجهز البيئة

---

### 📝 الخطوة 3: إضافة قاعدة بيانات PostgreSQL

#### 3.1 إضافة Database

1. في صفحة المشروع، اضغط "+ New"
2. اختر "Database"
3. اختر "Add PostgreSQL"
4. انتظر حتى يتم التجهيز (30-60 ثانية)

#### 3.2 ربط Database بالتطبيق

Railway يربط تلقائياً! سيوفر:
```env
DATABASE_URL=postgresql://postgres:password@containers-us-west-xxx.railway.app:5432/railway
```

#### 3.3 التحقق من الاتصال

```bash
# في Railway Dashboard → Database → Connect
# انسخ Connection URL وتحقق منه
```

---

### 📝 الخطوة 4: تكوين متغيرات البيئة

#### 4.1 الوصول إلى Variables

1. اضغط على خدمة التطبيق (Web Service)
2. انتقل إلى تبويب "Variables"
3. اضغط "+ New Variable"

#### 4.2 المتغيرات الإلزامية

##### SECRET_KEY

```bash
# توليد مفتاح جديد
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

أضف في Railway:
```
Name: SECRET_KEY
Value: django-insecure-abc123xyz789...
```

##### DEBUG

```
Name: DEBUG
Value: False
```

##### ALLOWED_HOSTS

```
Name: ALLOWED_HOSTS
Value: your-app.railway.app
```

**ملاحظة:** سيتم تحديث هذا تلقائياً بعد الحصول على النطاق.

#### 4.3 متغيرات المستخدم الإداري

```
Name: ADMIN_USERNAME
Value: admin

Name: ADMIN_EMAIL
Value: admin@iims.local

Name: ADMIN_PASSWORD
Value: SecurePassword123!

Name: ADMIN_JOB_NUMBER
Value: ADMIN-001

Name: ADMIN_RANK
Value: MIL

Name: ADMIN_FIRST_NAME
Value: System

Name: ADMIN_LAST_NAME
Value: Administrator
```

#### 4.4 متغيرات Groq AI (اختياري)

```
Name: GROQ_API_KEY
Value: YOUR_GROQ_API_KEY

Name: GROQ_MODEL
Value: llama-3.3-70b-versatile

Name: GROQ_REASONING_EFFORT
Value: medium

Name: GROQ_MAX_COMPLETION_TOKENS
Value: 8192

Name: GROQ_TEMPERATURE
Value: 0.3
```

#### 4.5 متغيرات الأداء (اختياري)

```
Name: WEB_CONCURRENCY
Value: 3

Name: PORT
Value: 8004
```

---

### 📝 الخطوة 5: النشر

#### 5.1 النشر التلقائي

Railway ينشر تلقائياً عند:
- Push جديد إلى GitHub
- تغيير في المتغيرات
- إعادة النشر يدوياً

#### 5.2 مراقبة عملية النشر

1. انتقل إلى تبويب "Deployments"
2. شاهد Logs المباشرة
3. انتظر حتى يظهر "✓ Success"

**مراحل النشر:**
```
1. 📦 Building...
   - Installing dependencies
   - Collecting static files
   - Running migrations

2. 🚀 Deploying...
   - Starting Gunicorn
   - Health checks

3. ✅ Success!
   - Application is live
```

#### 5.3 الحصول على URL

بعد النشر الناجح:
1. انتقل إلى تبويب "Settings"
2. قسم "Domains"
3. انسخ النطاق: `your-app.railway.app`

---

### 📝 الخطوة 6: التحقق من النشر

#### 6.1 فتح التطبيق

```
https://your-app.railway.app
```

#### 6.2 فحص الصحة

```
https://your-app.railway.app/health/
```

**الاستجابة المتوقعة:**
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

#### 6.3 تسجيل الدخول

```
https://your-app.railway.app/login/
```

استخدم:
- **Username**: `admin` (أو ما عينته في ADMIN_USERNAME)
- **Password**: كلمة المرور من ADMIN_PASSWORD

---

## إعداد قاعدة البيانات

### 🗄️ PostgreSQL على Railway

#### الوصول إلى Database

1. Dashboard → Database Service
2. تبويب "Data"
3. يمكنك تصفح الجداول مباشرة

#### الاتصال الخارجي

```bash
# الحصول على Connection String
# Dashboard → Database → Connect → External Connection

# مثال
psql postgresql://postgres:password@containers-us-west-xxx.railway.app:5432/railway
```

#### النسخ الاحتياطي

```bash
# تصدير قاعدة البيانات
pg_dump $DATABASE_URL > backup.sql

# استيراد قاعدة البيانات
psql $DATABASE_URL < backup.sql
```

#### المراقبة

Railway يوفر:
- **Metrics**: استخدام CPU/Memory
- **Logs**: سجلات قاعدة البيانات
- **Backups**: نسخ احتياطية تلقائية (في الخطط المدفوعة)

---

## تكوين المتغيرات

### 🔧 إدارة المتغيرات

#### إضافة متغير جديد

```bash
# عبر Railway CLI
railway variables set KEY=VALUE

# أو عبر Dashboard
Settings → Variables → + New Variable
```

#### تحديث متغير

```bash
# عبر CLI
railway variables set KEY=NEW_VALUE

# أو عبر Dashboard
Variables → Edit → Save
```

#### حذف متغير

```bash
# عبر CLI
railway variables delete KEY

# أو عبر Dashboard
Variables → Delete
```

#### استيراد من ملف

```bash
# إنشاء ملف .env.railway
cat > .env.railway << EOF
SECRET_KEY=your-secret-key
DEBUG=False
ADMIN_PASSWORD=your-password
EOF

# استيراد
railway variables set --from-file .env.railway
```

---

## النطاقات المخصصة

### 🌐 إضافة نطاق مخصص

#### الخطوة 1: إضافة النطاق في Railway

1. Settings → Domains
2. اضغط "+ Custom Domain"
3. أدخل نطاقك: `iims.example.com`
4. اضغط "Add Domain"

#### الخطوة 2: تكوين DNS

Railway سيعطيك CNAME record:

```
Type: CNAME
Name: iims (or @)
Value: your-app.railway.app
TTL: 3600
```

أضفه في DNS provider (Cloudflare, Namecheap, إلخ).

#### الخطوة 3: تحديث المتغيرات

```env
ALLOWED_HOSTS=iims.example.com,your-app.railway.app
CSRF_TRUSTED_ORIGINS=https://iims.example.com,https://your-app.railway.app
```

#### الخطوة 4: التحقق

```bash
# انتظر انتشار DNS (5-30 دقيقة)
nslookup iims.example.com

# اختبر الوصول
curl https://iims.example.com/health/
```

---

## المراقبة والصيانة

### 📊 مراقبة الأداء

#### Metrics Dashboard

Railway يوفر:
- **CPU Usage**: استخدام المعالج
- **Memory Usage**: استخدام الذاكرة
- **Network**: حركة البيانات
- **Response Time**: وقت الاستجابة

#### Logs

```bash
# عبر Dashboard
Deployments → View Logs

# عبر CLI
railway logs

# تصفية
railway logs --filter "ERROR"
```

#### Alerts

إعداد تنبيهات:
1. Settings → Notifications
2. أضف Webhook أو Email
3. اختر الأحداث (Deployment Failed, High CPU, إلخ)

---

### 🔄 التحديثات

#### تحديث تلقائي من GitHub

```bash
# في مستودع GitHub
git add .
git commit -m "Update feature"
git push origin main

# Railway ينشر تلقائياً
```

#### تحديث يدوي

```bash
# عبر CLI
railway up

# أو عبر Dashboard
Deployments → Redeploy
```

#### Rollback

```bash
# عبر Dashboard
Deployments → Previous Deployment → Redeploy

# أو عبر CLI
railway rollback
```

---

### 🗄️ صيانة قاعدة البيانات

#### تشغيل Migrations

```bash
# عبر Railway CLI
railway run python manage.py migrate

# أو أضف في startup.sh (موجود بالفعل)
```

#### إنشاء Superuser

```bash
# عبر CLI
railway run python manage.py createsuperuser

# أو استخدم ensure_admin (موجود في startup.sh)
```

#### تنظيف قاعدة البيانات

```bash
# حذف sessions قديمة
railway run python manage.py clearsessions

# تحسين قاعدة البيانات
railway run python manage.py dbshell
# ثم: VACUUM ANALYZE;
```

---

## استكشاف الأخطاء

### ❌ مشكلة: Application Error 503

**الأعراض:**
```
Application Error
Service Unavailable
```

**الحلول:**

1. **تحقق من Logs:**
   ```bash
   railway logs
   ```

2. **تحقق من DATABASE_URL:**
   ```bash
   railway variables
   # تأكد من وجود DATABASE_URL
   ```

3. **تحقق من Migrations:**
   ```bash
   railway run python manage.py showmigrations
   ```

4. **أعد النشر:**
   ```bash
   railway up --detach
   ```

---

### ❌ مشكلة: Database Connection Failed

**الأعراض:**
```
django.db.utils.OperationalError: could not connect to server
```

**الحلول:**

1. **تحقق من Database Service:**
   - Dashboard → Database
   - تأكد أنه يعمل (Status: Active)

2. **تحقق من DATABASE_URL:**
   ```bash
   railway variables get DATABASE_URL
   ```

3. **أعد تشغيل Database:**
   - Dashboard → Database → Settings → Restart

---

### ❌ مشكلة: Static Files لا تظهر

**الأعراض:**
- CSS/JS لا يعمل
- الصفحات تظهر بدون تنسيق

**الحلول:**

1. **تحقق من collectstatic:**
   ```bash
   railway run python manage.py collectstatic --noinput
   ```

2. **تحقق من WhiteNoise:**
   - تأكد من وجوده في `INSTALLED_APPS`
   - تأكد من وجوده في `MIDDLEWARE`

3. **تحقق من STATIC_ROOT:**
   ```bash
   railway run ls -la staticfiles/
   ```

---

### ❌ مشكلة: CSRF Verification Failed

**الأعراض:**
```
CSRF verification failed. Request aborted.
```

**الحلول:**

1. **تحديث CSRF_TRUSTED_ORIGINS:**
   ```env
   CSRF_TRUSTED_ORIGINS=https://your-app.railway.app
   ```

2. **تحقق من ALLOWED_HOSTS:**
   ```env
   ALLOWED_HOSTS=your-app.railway.app
   ```

3. **امسح Cookies:**
   - في المتصفح، امسح cookies للموقع

---

### ❌ مشكلة: Groq AI لا يعمل

**الأعراض:**
```
⚠️ خطأ في النظام: لا يمكن الاتصال بمحرك الذكاء الاصطناعي
```

**الحلول:**

1. **تحقق من GROQ_API_KEY:**
   ```bash
   railway variables get GROQ_API_KEY
   ```

2. **اختبر المفتاح:**
   ```bash
   curl https://api.groq.com/openai/v1/models \
     -H "Authorization: Bearer $GROQ_API_KEY"
   ```

3. **تحقق من التثبيت:**
   ```bash
   railway run pip list | grep groq
   ```

---

## 🎯 نصائح للأداء الأمثل

### 1. استخدم Connection Pooling

```python
# في settings.py (موجود بالفعل)
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600  # 10 دقائق
    )
}
```

### 2. قلل عدد Queries

```python
# استخدم select_related و prefetch_related
reports = IntelligenceReport.objects.select_related('source').all()
```

### 3. استخدم Caching

```python
# في settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}
```

### 4. ضبط Workers

```env
# للتطبيقات الصغيرة
WEB_CONCURRENCY=2

# للتطبيقات المتوسطة
WEB_CONCURRENCY=3

# للتطبيقات الكبيرة
WEB_CONCURRENCY=4
```

---

## 📞 الدعم

### الموارد

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **IIMS Docs**: [DEPLOYMENT.md](DEPLOYMENT.md)

### الحصول على المساعدة

1. **تحقق من Logs أولاً**
2. **راجع هذا الدليل**
3. **ابحث في Railway Discord**
4. **أنشئ Issue على GitHub**

---

## ✅ قائمة فحص النشر

- [ ] تم إنشاء حساب Railway
- [ ] تم ربط مستودع GitHub
- [ ] تم إضافة PostgreSQL Database
- [ ] تم توليد SECRET_KEY قوي
- [ ] تم تعيين DEBUG=False
- [ ] تم تكوين ALLOWED_HOSTS
- [ ] تم تكوين CSRF_TRUSTED_ORIGINS
- [ ] تم تعيين ADMIN_PASSWORD قوي
- [ ] تم تكوين GROQ_API_KEY (اختياري)
- [ ] تم النشر بنجاح
- [ ] تم اختبار /health/ endpoint
- [ ] تم اختبار تسجيل الدخول
- [ ] تم إعداد نطاق مخصص (اختياري)
- [ ] تم إعداد Monitoring/Alerts

---

**🎉 مبروك! تطبيق IIMS الآن يعمل على Railway!**

للمزيد من المعلومات، راجع:
- [DEPLOYMENT.md](DEPLOYMENT.md) - دليل النشر الشامل
- [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md) - توثيق المتغيرات
- [README.md](README.md) - نظرة عامة على المشروع
