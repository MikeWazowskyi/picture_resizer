# Picture Resizer

[![Django CI](https://github.com/MikeWazowskyi/picture_resizer/actions/workflows/django.yml/badge.svg)](https://github.com/MikeWazowskyi/picture_resizer/actions/workflows/django.yml)

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


### Request example

#### POST /api/resize_picture/

   Fields:
   * file - *.png, *.jpeg, *.jpg
   * width - width size to resize in px
   * height - height size to resize in px (optional)

multipart/form-data

```
   "file": my_favorite_picture.jpg
   "width": 100 
   "hight": 100
```

Response:

```
{
    "file": "http://<host>/mediafiles/images/default/my_favorite_picture.jpg",
    "resized": "http://<host>/mediafiles/images/resized/cb1b69b0a88d063616519790289cbba4_100x100.JPEG",
    "width": 100,
    "height": 148
}
```
