from django.db import models

from moderator.models import BaseTimestamp


class Doctor(BaseTimestamp):
    """
    Doctor model with OneToOne relation with custom user model.
    """
    user = models.OneToOneField("accounts.user", on_delete=models.CASCADE)
    specialization = models.CharField(max_length=64)
    info = models.TextField()

    class Meta:
        ordering = ['created_at']

    def __str__ (self):
        """
        Return doctor's email.
        """
        return self.user.email
