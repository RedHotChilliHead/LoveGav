from django.db import models


def playgrounds_photo_path(instance: "Playground", filename: str) -> str:
    return 'playgrounds/{town}/{filename}'.format(
        town=instance.town,
        filename=filename,
    )


class Playground(models.Model):
    town = models.CharField(max_length=100, blank=False)
    address = models.TextField(max_length=150, blank=False)
    description = models.CharField(max_length=200, null=False, blank=True)
    photo = models.ImageField(null=True, upload_to=playgrounds_photo_path)

    def __str__(self) -> str:
        return f"Playground({self.pk})"
