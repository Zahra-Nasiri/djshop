from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
import hashlib
from .exceptions import DuplicateImageException

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    image = models.ImageField(width_field='width', height_field='height')

    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)

    file_hash = models.CharField(max_length=40, db_index=True, editable=False)
    file_size = models.PositiveIntegerField(null=True, editable=False)

    focal_point_x = models.PositiveIntegerField(null=True, blank=True)
    focal_point_y = models.PositiveIntegerField(null=True, blank=True)
    focal_point_width = models.PositiveIntegerField(null=True, blank=True)
    focal_point_height = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *argws, **kwargs):
        self.file_size = self.image.size

        hasher = hashlib.sha1()
        for chunk in self.image.file.chunks():
            hasher.update(chunk)

        self.file_hash = hasher.hexdigest()

        super().save(*argws, **kwargs)


@receiver(pre_save, sender=Image)
def check_duplication_hash(sender, instance, **kwargs):
    existed = Image.objects.filter(file_hash=instance.file_hash).exists()
    if existed:
        raise DuplicateImageException("Duplicate")