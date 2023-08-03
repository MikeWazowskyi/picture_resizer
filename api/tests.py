import shutil
import tempfile
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework import status
from rest_framework.reverse import reverse

from picture.models import Picture


class PictureViewTestCase(TestCase):
    TMP_MEDIA_ROOT = tempfile.mkdtemp(prefix='test_media')

    def setUp(self):
        self.url = reverse('resize_image')
        self.picture_high = 800
        self.picture_width = 800
        self.width = 600
        self.height = 600
        self.tmp_image = self.create_temp_image()
        self.data = {
            'file': self.tmp_image,
            'width': self.width,
            'height': self.height,
        }
        self.no_high_data = {
            'file': self.tmp_image,
            'width': self.width,
        }

    def create_temp_image(self):
        image = Image.new('RGB', (self.picture_high, self.picture_width))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=True)
        image.save(tmp_file, format='PNG')
        tmp_file.seek(0)
        return SimpleUploadedFile(tmp_file.name, tmp_file.read(),
                                  content_type='image/png')

    def tearDown(self):
        shutil.rmtree(self.TMP_MEDIA_ROOT, ignore_errors=True)

    @override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
    def test_create_new_picture_response_ok(self):
        response = self.client.post(self.url, self.data,
                                    format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
    def test_create_new_picture_save_data_in_database(self):
        self.client.post(self.url, self.data, format='multipart')
        self.assertEqual(Picture.objects.count(), 1)

    @override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
    def test_resized_picture_has_correct_name(self):
        self.client.post(self.url, self.data, format='multipart')

        picture = Picture.objects.first()
        expected_file_name = Picture(**self.data).generate_file_name
        new_file_name = Path(str(picture.resized_image)).name
        self.assertEqual(new_file_name, expected_file_name)

    @override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
    def test_resized_picture_has_proper_size(self):
        self.client.post(self.url, self.data, format='multipart')
        picture = Picture.objects.first()
        resized_image = Image.open(picture.resized_image.path)
        self.assertEqual(resized_image.width, self.width)
        self.assertEqual(resized_image.height, self.height)

    @override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
    def test_create_new_picture_with_no_high_response_ok(self):
        response = self.client.post(self.url, self.no_high_data,
                                    format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
    def test_create_new_picture_with_no_high_has_correct_size(self):
        self.client.post(self.url, self.no_high_data,
                         format='multipart')
        picture = Picture.objects.first()
        expected_height = int(
            self.picture_high / self.picture_width * self.width
        )
        self.assertEqual(picture.height, expected_height)

    @override_settings(MEDIA_ROOT=TMP_MEDIA_ROOT)
    def test_create_existing_picture(self):
        Picture.objects.create(**self.data)

        response = self.client.post(self.url, self.data,
                                    format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Picture.objects.count(), 1)
