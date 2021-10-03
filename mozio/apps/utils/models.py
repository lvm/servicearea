import time
import datetime
from django.db import models
from django.template.defaultfilters import slugify


class TimestampMixinModel(models.Model):
    "Simply keeps track of time"
    created_at = models.DateTimeField(
        editable=False, auto_now_add=True, null=True, blank=True
    )
    updated_at = models.DateTimeField(
        editable=False, auto_now=True, null=True, blank=True
    )

    class Meta:
        abstract = True


class NamedMixinModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.name

    def url_app_model(self):
        return "{}_{}".format(self._meta.app_label, self._meta.model_name)

    def get_admin_url(self):
        return reverse(f"admin:{self.url_app_model()}_change", args=[self.pk])

    def _generate_unique_slug(self, string):
        def now():
            return int(time.mktime(datetime.datetime.now().timetuple()))

        slug = slugify(string)
        slug_ = slug
        while self._meta.model.objects.filter(slug=slug_).exists():
            slug_ = f"{slug}-{now()}"
        slug = slug_

        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug(self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
