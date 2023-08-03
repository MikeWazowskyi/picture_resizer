from pathlib import Path
from io import BytesIO
from hashlib import md5
from django.db import models
from PIL import Image as PilImage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import pre_save
from django.dispatch import receiver


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

    def resize_image(self, file_name):
        image = PilImage.open(self.file)
        if self.height is None:
            self.height = int(image.height / image.width * self.width)
        resized_image = image.resize((self.width, self.height))
        output = BytesIO()
        resized_image.save(output, format=image.format, quality=100)
        output.seek(0)
        self.resized_image = InMemoryUploadedFile(
            output, 'ImageField',
            file_name,
            'image/jpeg', output.getbuffer().nbytes, None
        )

    @property
    def generate_file_name(self):
        file_path = Path(self.file.name)
        return (f'{md5(file_path.name.encode()).hexdigest()}_'
                f'{self.width}x{self.height}{file_path.suffix}')


@receiver(pre_save, sender=Picture)
def pre_save_picture(sender, instance, **kwargs):
    if not instance.resized_image:
        instance.resize_image(instance.generate_file_name)
