# ANNit

Hi Joe,

ANNit was implemented with Django.
To install Django, see this page:
https://docs.djangoproject.com/en/3.0/topics/install/

I followed this tutorial:
https://docs.djangoproject.com/en/3.0/intro/tutorial03/

--

run the server:
python manage.py runserver
And you will see the interact at http://127.0.0.1:8000/
-
0) Welcome page -> start1
1) LOAD a file: for example the SA2_4.nodes.csv as I attached in this directory
2) insert some labels/annotations. Remember to refresh the page after your final insertion.
3) Then you can start from the first entry all the way to the end.
4) The current implementation loops at the last entry when you click 'next'. So just click 'go back to index' when you are done.
5) Sometimes the export function doesn't work well (I don't know why). So the actual directory is printed in the console.

6)Well, I suggest you play with the example file SA2_4.nodes.csv first.

--
In case you want to change something directly in the databse, just go to
http://127.0.0.1:8000/admin


-

In case you want to change the model.py file
for updating the database:

python manage.py migrate
python manage.py makemigrations annotate
python manage.py sqlmigrate annotate 0001
