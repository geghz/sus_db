#!/usr/bin/env python3
"""
bootstrap.py — Полная автоматическая генерация проекта "СУБД сотрудников"
Создаёт:
- venv и устанавливает Python‑зависимости
- Django‑проект в backend/ и приложения
- Файлы настроек с динамическими ролями
- React‑frontend (если есть npx) с базовой структурой
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

BASE = Path(__file__).parent.resolve()
print(f"Bootstrapping project at {BASE}\n")

def run(cmd, cwd=None):
    print("▶", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=cwd or str(BASE))

# 1) Write requirements.txt
print("1) Writing requirements.txt")
requirements = [
    "Django==4.2.6\n",
    "djangorestframework==3.14.0\n",
    "djangorestframework-simplejwt==5.2.2\n",
    "django-environ==0.10.0\n",
    "django-filter==23.2\n",
    "django-cors-headers==3.14.0\n",
    "openpyxl==3.1.2\n",
    "Pillow==10.0.0\n",
    "pytest==7.4.0\n",
    "pytest-django==4.5.2\n",
]
(BASE / "requirements.txt").write_text("".join(requirements))

# 2) Create virtual environment and install dependencies
print("\n2) Creating virtual environment and installing dependencies")
run([sys.executable, "-m", "venv", "venv"])
# Determine python in venv
if os.name == "nt":
    venv_py = BASE / "venv" / "Scripts" / "python.exe"
else:
    venv_py = BASE / "venv" / "bin" / "python"
# Upgrade pip, setuptools, wheel
run([str(venv_py), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
# Install requirements
run([str(venv_py), "-m", "pip", "install", "-r", "requirements.txt"])

# 3) Generate Django project
print("\n3) Generating Django project")
backend = BASE / "backend"
backend.mkdir(exist_ok=True)
run([str(venv_py), "-m", "django", "startproject", "sus_project", str(backend)])

# 4) Create Django apps
print("\n4) Creating Django apps")
apps = ["employees", "documents", "tags", "notifications", "dashboard", "roles"]
for app in apps:
    app_dir = backend / app
    if not app_dir.exists():
        run([str(venv_py), str(backend / "manage.py"), "startapp", app], cwd=str(backend))
    # ensure __init__.py
    (app_dir / "__init__.py").write_text("")
    # migrations
    mig = app_dir / "migrations"
    mig.mkdir(exist_ok=True)
    (mig / "__init__.py").write_text("")
    # scaffold serializers, views, urls, admin
    (app_dir / "serializers.py").write_text("# TODO: define serializers for " + app + "\n")
    (app_dir / "views.py").write_text("# TODO: define viewsets for " + app + "\n")
    (app_dir / "urls.py").write_text(
        "from django.urls import path, include\n"
        "from rest_framework.routers import DefaultRouter\n"
        "# TODO: import your viewsets\n\n"
        "router = DefaultRouter()\n"
        "# router.register(...)\n\n"
        "urlpatterns = [\n"
        "    path('api/" + app + "/', include(router.urls)),\n"
        "]\n"
    )
    (app_dir / "admin.py").write_text("# TODO: register models for " + app + "\n")

# 5) Write .env.example
print("\n5) Writing .env.example")
env_lines = [
    "DEBUG=True\n",
    "SECRET_KEY=change-me-please-replace\n",
    "ALLOWED_HOSTS=localhost,127.0.0.1\n",
]
(backend / "sus_project" / ".env.example").write_text("".join(env_lines))

# 6) settings.py with dynamic roles app
print("\n6) Writing settings.py")
settings_lines = [
    "from pathlib import Path",
    "import os",
    "import environ",
    "",
    "BASE_DIR = Path(__file__).resolve().parent.parent",
    "env = environ.Env()",
    "environ.Env.read_env(os.path.join(BASE_DIR, 'sus_project/.env'))",
    "",
    "SECRET_KEY = env('SECRET_KEY')",
    "DEBUG = env.bool('DEBUG', default=False)",
    "ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])",
    "",
    "INSTALLED_APPS = [",
    "    'django.contrib.admin',",
    "    'django.contrib.auth',",
    "    'django.contrib.contenttypes',",
    "    'django.contrib.sessions',",
    "    'django.contrib.messages',",
    "    'django.contrib.staticfiles',",
    "    'rest_framework',",
    "    'rest_framework_simplejwt',",
    "    'django_filters',",
    "    'corsheaders',",
] 
for app in apps:
    settings_lines.append(f"    '{app}',")
settings_lines += [
    "]",
    "",
    "MIDDLEWARE = [",
    "    'corsheaders.middleware.CorsMiddleware',",
    "    'django.middleware.security.SecurityMiddleware',",
    "    'django.contrib.sessions.middleware.SessionMiddleware',",
    "    'django.middleware.common.CommonMiddleware',",
    "    'django.middleware.csrf.CsrfViewMiddleware',",
    "    'django.contrib.auth.middleware.AuthenticationMiddleware',",
    "    'django.contrib.messages.middleware.MessageMiddleware',",
    "    'django.middleware.clickjacking.XFrameOptionsMiddleware',",
    "]",
    "",
    "ROOT_URLCONF = 'sus_project.urls'",
    "",
    "TEMPLATES = [",
    "    {",
    "        'BACKEND': 'django.template.backends.django.DjangoTemplates',",
    "        'DIRS': [],",
    "        'APP_DIRS': True,",
    "        'OPTIONS': {",
    "            'context_processors': [",
    "                'django.template.context_processors.debug',",
    "                'django.template.context_processors.request',",
    "                'django.contrib.auth.context_processors.auth',",
    "                'django.contrib.messages.context_processors.messages',",
    "            ],",
    "        },",
    "    },",
    "]",
    "",
    "WSGI_APPLICATION = 'sus_project.wsgi.application'",
    "",
    "DATABASES = {",
    "    'default': {",
    "        'ENGINE': 'django.db.backends.sqlite3',",
    "        'NAME': BASE_DIR / 'db.sqlite3',",
    "    }",
    "}",
    "",
    "AUTH_USER_MODEL = 'employees.CustomUser'",
    "",
    "REST_FRAMEWORK = {",
    "    'DEFAULT_AUTHENTICATION_CLASSES': (",
    "        'rest_framework_simplejwt.authentication.JWTAuthentication',",
    "    ),",
    "    'DEFAULT_PERMISSION_CLASSES': (",
    "        'rest_framework.permissions.IsAuthenticated',",
    "    ),",
    "    'DEFAULT_FILTER_BACKENDS': (",
    "        'django_filters.rest_framework.DjangoFilterBackend',",
    "    ),",
    "}",
    "",
    "STATIC_URL = '/static/'",
]
(backend / "sus_project" / "settings.py").write_text("\n".join(settings_lines))

# 7) Scaffold roles app
print("\n7) Scaffold roles app code")
roles = backend/"roles"
(roles/"models.py").write_text("""\
from django.db import models

class Permission(models.Model):
    codename=models.SlugField(max_length=50,unique=True)
    name=models.CharField(max_length=100)
    def __str__(self): return self.name

class Role(models.Model):
    name=models.CharField(max_length=50,unique=True)
    permissions=models.ManyToManyField(Permission,blank=True)
    def __str__(self): return self.name
""")
(roles/"serializers.py").write_text("""\
from rest_framework import serializers
from .models import Permission,Role

class PermissionSerializer(serializers.ModelSerializer):
    class Meta: model=Permission; fields=['id','codename','name']

class RoleSerializer(serializers.ModelSerializer):
    permissions=PermissionSerializer(many=True)
    class Meta: model=Role; fields=['id','name','permissions']
""")
(roles/"views.py").write_text("""\
from rest_framework import viewsets
from .models import Permission,Role
from .serializers import PermissionSerializer,RoleSerializer

class PermissionViewSet(viewsets.ModelViewSet):
    queryset=Permission.objects.all(); serializer_class=PermissionSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset=Role.objects.all(); serializer_class=RoleSerializer
""")
(roles/"urls.py").write_text("""\
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import PermissionViewSet,RoleViewSet
router=DefaultRouter()
router.register('permissions',PermissionViewSet)
router.register('roles',RoleViewSet)
urlpatterns=[path('api/roles/',include(router.urls))]
""")
(roles/"admin.py").write_text("""\
from django.contrib import admin
from .models import Permission,Role

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display=('codename','name')
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display=('name',); filter_horizontal=('permissions',)
""")

# 8) CustomUser in employees
print("\n8) CustomUser in employees")
emp = backend/"employees"
(emp/"models.py").write_text("""\
from django.contrib.auth.models import AbstractUser
from django.db import models
from roles.models import Role

class CustomUser(AbstractUser):
    roles=models.ManyToManyField(Role,blank=True)
    def has_perm(self,perm,obj=None):
        return self.roles.filter(permissions__codename=perm).exists() or super().has_perm(perm,obj)
""")
(emp/"admin.py").write_text("""\
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets=UserAdmin.fieldsets+(('Roles',{'fields':('roles',)}),)
    filter_horizontal=('roles',)
""")

# 9) sus_project/urls.py
print("\n9) Writing sus_project/urls.py")
(backend/"sus_project"/"urls.py").write_text("""\
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns=[
    path('admin/',admin.site.urls),
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('',include('roles.urls')),
    path('',include('employees.urls')),
    path('',include('documents.urls')),
    path('',include('tags.urls')),
    path('',include('notifications.urls')),
    path('',include('dashboard.urls')),
]
""")

# 10) React frontend
print("\n10) Scaffolding React frontend")
npx_exec = shutil.which("npx") or shutil.which("npx.cmd")
if npx_exec:
    run([npx_exec,"create-react-app","frontend"])
    fr=BASE/"frontend"
    npm_exec=shutil.which("npm") or shutil.which("npm.cmd")
    if npm_exec:
        deps=["@mui/material@5","@mui/icons-material@5","@emotion/react","@emotion/styled","axios","react-router-dom","http-proxy-middleware"]
        run([npm_exec,"install"]+deps,cwd=str(fr))
    # setupProxy.js
    (fr/"src"/"setupProxy.js").write_text("""\
const {{ createProxyMiddleware }} = require('http-proxy-middleware');
module.exports=function(app){app.use('/api',createProxyMiddleware({target:'http://localhost:8000',changeOrigin:true}));};
""")
    # api.js, contexts, App, index, components (omitted for brevity)
else:
    print("⚠ npx not found — frontend skipped")

print("\n✅ Bootstrap complete!")

