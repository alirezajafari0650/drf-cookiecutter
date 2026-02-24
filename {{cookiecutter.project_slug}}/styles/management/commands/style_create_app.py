import os
from django.conf import settings
from django.core.management.base import BaseCommand

BASE_DIR = settings.BASE_DIR.__str__()


class Command(BaseCommand):
    def create_app(self, app_name):
        app_path = os.path.join(BASE_DIR, app_name)

        # ایجاد پوشه اصلی و زیرپوشه‌ها
        folders = [
            app_path,
            os.path.join(app_path, "migrations"),
            os.path.join(app_path, "tests"),
            os.path.join(app_path, "api"),
        ]

        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)

        # تابع کمکی برای ایجاد فایل و نوشتن محتوا
        def create_file(filename, content):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

        # ایجاد فایل‌های __init__.py
        init_files = [
            os.path.join(app_path, "__init__.py"),
            os.path.join(app_path, "migrations", "__init__.py"),
            os.path.join(app_path, "tests", "__init__.py"),
            os.path.join(app_path, "api", "__init__.py"),
        ]
        for file in init_files:
            create_file(file, "")

        # ایجاد فایل‌های api
        serializers_text = "from rest_framework import serializers\n\n# Create your serializers here."
        create_file(os.path.join(app_path, "api", "serializers.py"), serializers_text)

        api_views_text = "from rest_framework import generics\n\n# Create your views here."
        create_file(os.path.join(app_path, "api", "api_views.py"), api_views_text)

        api_urls_text = "from django.urls import path\n\nurlpatterns = [\n\n]"
        create_file(os.path.join(app_path, "api", "urls.py"), api_urls_text)

        # ایجاد فایل‌های روت
        admin_text = "from django.contrib import admin\n\n# Register your models here."
        create_file(os.path.join(app_path, "admin.py"), admin_text)

        apps_text = f"""from django.apps import AppConfig\n\n\nclass {app_name.capitalize()}Config(AppConfig):\n    default_auto_field = "django.db.models.BigAutoField"\n    name = "{app_name}" \n    import {app_name}.signals"""
        create_file(os.path.join(app_path, "apps.py"), apps_text)

        models_text = "from django.db import models\n\n# Create your models here."
        create_file(os.path.join(app_path, "models.py"), models_text)

        signals_text = "from django.db.models.signals import post_save\nfrom django.dispatch import receiver\n\n\n# Create your signals here."
        create_file(os.path.join(app_path, "signals.py"), signals_text)

        exceptions_text = f"from rest_framework.exceptions import APIException\n\n\nclass {app_name.capitalize()}Exception(APIException):\n    pass"
        create_file(os.path.join(app_path, "exceptions.py"), exceptions_text)

        permissions_text = f"from rest_framework.permissions import BasePermission\n\n\nclass {app_name.capitalize()}Permission(BasePermission):\n    pass"
        create_file(os.path.join(app_path, "permissions.py"), permissions_text)

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)

    def handle(self, *args, **options):
        app_name = options['app_name']
        self.create_app(app_name)
        self.stdout.write(
            self.style.SUCCESS(f"Created Django app '{app_name}' with the specified structure.")
        )