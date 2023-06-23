from io import BytesIO
from hashlib import md5
from django.db import models
from PIL import Image as PilImage
from django.core.files.uploadedfile import InMemoryUploadedFile


class Picture(models.Model):
    file = models.ImageField(
        upload_to='images/default/',
        default=None
    )
    resized_image = models.ImageField(
        upload_to='images/resized/',
        null=True,
        blank=True,
    )
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def resize_image(self):
        if not self.resized_image:
            image = PilImage.open(self.file)
            if self.height is None:
                self.height = int(image.height / image.width * self.width)
            resized_image = image.resize((self.width, self.height))
            output = BytesIO()
            resized_image.save(output, format=image.format, quality=100)
            output.seek(0)
            original_file_name = self.file.name.split(".")[0]
            file_name = (f'{md5(original_file_name.encode()).hexdigest()}_'
                         f'{self.width}x{self.height}.{image.format}')
            self.resized_image = InMemoryUploadedFile(
                output, 'ImageField',
                file_name,
                'image/jpeg', output.getbuffer().nbytes, None
            )
            super().save()
