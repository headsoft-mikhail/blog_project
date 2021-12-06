echo "MAKEMIGRATIONS"
python manage.py makemigrations
echo "MIGRATE"
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('userUsername', 'userEmail', 'userPassword')" | python manage.py shell
echo "START GUNICORN"
gunicorn blog_api.wsgi -w 4 -b 0.0.0.0:8000

