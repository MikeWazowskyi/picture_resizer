import base64

from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from rest_framework import serializers

from picture.models import Picture


class Base64ImageField(serializers.ImageField):
    """Image custom field."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            img_format, img_str = data.split(';base64,')
            ext = img_format.split('/')[-1]

            data = ContentFile(base64.b64decode(img_str),
                               name='temp.' + ext)

        return super().to_internal_value(data)


class PositiveIntegerField(serializers.IntegerField):
    MINIMAL_VALUE = 1
    default_error_messages = {
        'invalid': 'Enter a positive integer value.',
        'min_value': (f'Ensure this value is greater'
                      f' than or equal to {MINIMAL_VALUE}.'),
    }

    def __init__(self, **kwargs):
        validators = kwargs.get('validators', list())
        validators.append(
            MinValueValidator(self.MINIMAL_VALUE),
        )
        kwargs['validators'] = validators
        super().__init__(**kwargs)


class PictureSerializer(serializers.ModelSerializer):
    file = Base64ImageField()
    resized = Base64ImageField(source='resized_image', required=False)
    width = PositiveIntegerField()
    height = PositiveIntegerField(required=False)

    class Meta:
        model = Picture
        fields = ('file', 'resized', 'width', 'height')
        write_only_fields = ('file', 'width', 'height')
        read_only_fields = ('resized',)
