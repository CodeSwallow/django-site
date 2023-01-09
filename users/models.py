from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user for easier modification."""

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'
