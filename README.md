# picture_resizer

## Description

#### Implementation of a simple Django RESTfull server, which make resize of pictures.

## Instructions for running

1. Clone the repository and navigate to it in the command line::

   ``` git clone https://github.com/MikeWazowskyi/picture_resizer```

   ``` cd picture_resizer```

2. Create and activate a virtual environment:

   ```python -m venv venv```
   
   *unix:
   ```source venv/Scripts/activate``` 
   
   Windows:
   ```./venv/Scripts/activate``` 
   
3. Install requirements:

   ``` python -m pip install --upgrade pip```

   ``` python -m pip install -r requirements.txt```
   
4. Make migrations:

   ``` python manage.py migrate```

5. Run application on dev server:

   ``` python manage.py runserver```
