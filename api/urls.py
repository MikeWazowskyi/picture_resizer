from django.urls import path

from api import views as api_views

urlpatterns = [
    path("resize_picture/",
         api_views.PictureView.as_view(),
         name='resize_image',
         ),
]


