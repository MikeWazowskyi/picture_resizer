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
        search_params = dict(
            file__contains=request.data.get('file'),
            width=int(request.data.get('width')),
        )
        if 'height' in request.data:
            search_params['height'] = int(request.data.get('height'))

        image = Picture.objects.filter(**search_params).first()
        if image:
            serializer = self.get_serializer(image)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            )
        return super().create(request, *args, **kwargs)
