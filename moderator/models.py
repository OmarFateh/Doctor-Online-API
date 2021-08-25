from django.db import models


class BaseTimestamp(models.Model):
    """
    Timestamp abstract model to be inherited from.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class Moderator(BaseTimestamp):
    """
    Moderator model with OneToOne relation with custom user model.
    """
    user = models.OneToOneField("accounts.user", on_delete=models.CASCADE)

    def __str__ (self):
        # Return moderator's email.
        return self.user.email
