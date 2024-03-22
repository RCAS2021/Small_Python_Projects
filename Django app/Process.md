https://docs.djangoproject.com/en/5.0/intro/tutorial01/ <- tutorial01

# Installing django
py -m pip install Django==5.0.3 (Latest official version)

# Verifying django version
py -m django --version

# Creating project
Start project, creates folders
    django-admin startproject mysite
    -> will create project folder with __init__.py, asgi.py, settings.py, urls.py, wsgi.py and manage.py

# Development server
Switch to outer project folder
    cd mysite
Run server
    py manage.py runserver
    -> By default starts the server on port 8000, to change server's port, put it after runserver

# Creating the polls app
Make sure you are in the same folder as manage.py
##  Create app 
        py manage.py startapp polls
        -> Will create project folder, migrations folder with __init__.py, __init__.py, admin.py, apps.py, models.py, tests.py, views.py

# Writing first views
Go to views.py
Write view code

# Calling the view
## Creating and URLconf
    Create file urls.py
    Write code in polls/urls.py
    Go to mysite/urls.py
    Write code in urls.py
    Check if its working
        py manage.py runserver
        go to localhost:8000/polls

# Setting up database
Go to mysite/settings.py
Edit database engine and name if necessary -> https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-DATABASES
Set time_zone to your time zone
## Creating tables in database
        python manage.py migrate

# Creating models
##  Creating models Question and Choice in polls/models.py
        Write models code

# Activating models
##  Include app in project
        Add polls config to mysite/settings.py installed_apps -> 'polls.apps.PollsConfig'
        Run python manage.py makemigrations polls
        Check what SQL the command migrate would run
            python manage.py sqlmigrate polls 0001
            -> Can also run python manage.py check to check for errors without migrating or touching the database
        Run migrate to create the model tables
            python manage.py migrate

# Playing with the app
Enter interative python shell
    python manage.py shell
Explore database API -> https://docs.djangoproject.com/en/5.0/topics/db/queries/
In shell enter:

    >>> from polls.models import Choice, Question -> Import the models classes
    >>> Question.objects.all() -> No questions in the system yet
    >>> from django.utils import timezone -> importing timezone methods
    >>> q = Question(question_text="What's new?", pub_date=timezone.now()) -> Create new question
    >>> q.save() -> Save question in database
    >>> q.id -> Returns question id
    >>> q.question_text -> Returns question text
    >>> q.pub_date -> Returns question publication date
    >>> q.question_text = "What's up?" -> Using save, changes the value
    >>> q.save()
    >>> Question.objects.all() -> Displays all questions in the database
##  Better representing objects
        Go to polls/models.py
        Add __str__ to both methods
        Add custom method to model
        Enter shell again and run:
        >>> from polls.models import Choice, Question -> Import the models classes
        >>> Question.objects.all() -> Display questions in database to check if modification worked
        >>> Question.objects.filter(id=1) -> Filter question
        >>> Question.objects.filter(question_text__startswith="What") -> Another filter, note the __ instead of _ on startswith
        >>> from django.utils import timezone -> Importing timezone
        >>> current_year = timezone.now().year -> Get current year
        >>> Question.objects.get(pub_date__year=current_year) -> Gets questions in current year, note the __ instead of _ on year
        >>> Question.objects.get(id=2) -> Get question with id that does not exist raises an exception
        >>> Question.objects.get(pk=1) -> Gets by primary key
        >>> q = Question.objects.get(pk=1) -> Assigning the question with pk = 1 to q
        >>> q.was_published_recently() -> Check if the custom method worked
        >>> q.choice_set.all() -> Checks if question has choices
        >>> q.choice_set.create(choice_text="Not much", votes=0) -> Creating choices for the question
        >>> q.choice_set.create(choice_text="The sky", votes=0) -> Creating choices for the question
        >>> c = q.choice_set.create(choice_text="Nothing", votes=0) -> Creating choices for the question
        >>> c.question -> Choice objects have API access to their related question
        >>> q.choice_set.all() -> Checks choices, question has access to choices
        >>> q.choice_set.count() -> Counts number of choices in question
        >>> Choice.objects.filter(question__pub_date__year=current_year) -> API automatically follows relationships, use __ to separate relationships
        >>> c = q.choice_set.filter(choice_text__startswith="The") -> Selecting choice to later delete
        >>> c.delete() -> Deleting selected choice
