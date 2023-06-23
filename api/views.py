import logging

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.serializers import PictureSerializer
from picture.models import Picture

logger = logging.getLogger(__name__)


class PictureView(CreateAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def create(self, request, *args, **kwargs):
        logger.info(f'Request: {request.method} {request.path}')
        if 'height' in request.data:
            image = Picture.objects.filter(
                file__contains=request.data.get('file'),
                width=int(request.data.get('width')),
                height=int(request.data.get('height'))
            )
        else:
            image = Picture.objects.filter(
                file__contains=request.data.get('file'),
                width=int(request.data.get('width')),
            ).first()
        if image:
            serializer = self.get_serializer(image)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            )
        return super().create(request, *args, **kwargs)
