import os
import django
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voenkom.settings')
django.setup()

User = get_user_model()

username = "raul245"
email = "kirillmendrin245@yandex.com"
password = "viper2018"

try:
    User.objects.create_superuser(username=username, email=email,
                                  password=password)
    print(f"✅ Суперпользователь '{username}' успешно создан.")
except IntegrityError:
    print(f"⚠️ Суперпользователь '{username}' уже существует.")
