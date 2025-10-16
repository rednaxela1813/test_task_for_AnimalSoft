# test_task_for_AnmalSoft
This is a simple skeleton project for downloading RSS articles. Download the project to your computer as usual. Create a .env file with your variables. In the admin panel, create a resource from which you want to download articles. 


cd project
pip install -r requirements.txt
touch .env # add your secrets
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

Add News path RSS to admin panel NewsSource then


python manage.py fetch_articles

new articles will add to Articals molel