import secrets

from django.core.validators import URLValidator
from django.db import models, IntegrityError, transaction


def default_shortened_url():
    return secrets.token_urlsafe(8)


class ShortenedURL(models.Model):
    # Expanded URL is a TextField because it can contain really long URLs
    expanded_url = models.TextField(validators=[URLValidator])
    # The shortened URL must be unique, as it'll be the key to the expanded url
    shortened_url = models.CharField(max_length=20,
                                     unique=True,
                                     default=default_shortened_url)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        with transaction.atomic() as atomic:
            try:
                retry = False
                super(ShortenedURL, self).save(
                    force_insert, force_update, using, update_fields)
            except IntegrityError:
                # In case there is an integrity error, it should be due to the
                # uniqueness flaw on the shortened_url field. In that case
                # call self.save again in order to retry it.
                #
                # This should be more efficient in terms of database usage than
                # querying everytime before saving.
                if not self.id:
                    retry = True

        if retry:
            self.shortened_url = default_shortened_url()
            self.save(force_insert, force_update, using, update_fields)
